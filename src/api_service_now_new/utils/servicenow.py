import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import polars as pl
import requests
from django.db import transaction
from django.utils import timezone as dj_timezone


def get_servicenow_env() -> Tuple[str, Tuple[str, str], Dict[str, str]]:
    """Retorna (base_url, (user, password), headers) usando variáveis de ambiente.

    Espera encontrar `SERVICE_NOW_BASE_URL`, `SERVICE_NOW_USERNAME` e `SERVICE_NOW_USER_PASSWORD` no env.
    """
    base_url = os.getenv("SERVICE_NOW_BASE_URL")
    user = os.getenv("SERVICE_NOW_USERNAME")
    password = os.getenv("SERVICE_NOW_USER_PASSWORD")
    headers = {"Content-Type": "application/json"}
    if not all([base_url, user, password]):
        raise RuntimeError(
            "Missing ServiceNow credentials in environment variables"
        )
    # Informar ao verificador de tipos que as variáveis não são None aqui
    assert base_url is not None and user is not None and password is not None
    return base_url, (user, password), headers


def ensure_datetime(s: str, end: bool = False) -> str:
    """Mantido apenas por compatibilidade (não faz parsing real, apenas completa HH:MM:SS se formato for YYYY-MM-DD)."""
    if isinstance(s, str) and len(s) == 10:
        return f"{s} 23:59:59" if end else f"{s} 00:00:00"
    return s


def paginate(
    path: str,
    params: Optional[Dict] = None,
    limit: int = 10000,
    mode: str = "offset",
    limit_param: str = "sysparm_limit",
    offset_param: str = "sysparm_offset",
    cursor_param: str = "startingAfter",
    cursor_field: Optional[str] = None,
    result_key: str = "result",
) -> List[Dict]:
    """Paginação genérica para APIs REST.

    - `mode` pode ser "offset" (usa `limit_param` e `offset_param`) ou "cursor" (usa `cursor_param`).
    - `path` é concatenado a `base_url` como f"{base_url}/{path}".
    - `params` contém query params fixos (ex: {'sysparm_query': '...'}).
    - `cursor_field` (opcional) indica qual campo do último item usar como próximo cursor.

    Retorna lista completa de itens obtidos via `result_key` no JSON.
    """
    all_results = []
    params = dict(params or {})

    # sempre pega env internamente (simplifica chamadas)
    base_url, auth, headers = get_servicenow_env()

    if mode == "offset":
        offset = 0
        while True:
            params_local = dict(params)
            params_local[limit_param] = limit
            params_local[offset_param] = offset

            resp = requests.get(
                f"{base_url}/{path}",
                auth=auth,
                headers=headers,
                params=params_local,
            )
            if resp.status_code != 200:
                raise RuntimeError(
                    f"API error: {resp.status_code} - {resp.text}"
                )

            page = resp.json().get(result_key, [])
            if not page:
                break

            all_results.extend(page)
            offset += limit
            print(offset)

    elif mode == "cursor":
        cursor = None
        while True:
            params_local = dict(params)
            params_local["perPage"] = limit
            if cursor:
                params_local[cursor_param] = cursor

            resp = requests.get(
                f"{base_url}/{path}",
                auth=auth,
                headers=headers,
                params=params_local,
            )
            if resp.status_code != 200:
                raise RuntimeError(
                    f"API error: {resp.status_code} - {resp.text}"
                )

            page = resp.json().get(result_key, [])
            if not page:
                break

            all_results.extend(page)

            if cursor_field:
                last = page[-1]
                cursor = last.get(cursor_field)
                if not cursor:
                    break
            else:
                # sem campo de cursor, não sabemos como continuar
                break

    else:
        raise ValueError(
            "Unsupported pagination mode: must be 'offset' or 'cursor'"
        )

    # Se não houver resultados, retornar lista vazia
    if not all_results:
        return []

    # 1) Achatar referências e coletar todas as chaves existentes
    processed = []
    all_keys = set()
    for result in all_results:
        if not result:
            continue
        flat = flatten_reference_fields(dict(result))
        processed.append(flat)
        all_keys.update(flat.keys())

    # garantir chaves de audit/etl
    all_keys.update({"etl_created_at", "etl_updated_at"})

    # 2) Normalizar: para cada registro, garantir todas as chaves e coerir valores
    normalized = []
    for r in processed:
        row = {}
        for k in all_keys:
            v = r.get(k)
            if v is None:
                row[k] = None
            else:
                # strings vazias viram None
                if isinstance(v, str) and v.strip() == "":
                    row[k] = None
                else:
                    try:
                        row[k] = str(v)
                    except Exception:
                        row[k] = None
        # etl timestamps: usar ISO strings para evitar tipos datetime mistos
        now_iso = dj_timezone.now().isoformat()
        row["etl_created_at"] = now_iso
        row["etl_updated_at"] = now_iso
        normalized.append(row)

    return normalized


def process_data(data: List[Dict]) -> List[Dict]:
    """Mantido para compatibilidade; agora apenas achata refs e retorna strings/None sem parse de datas."""
    out = []
    for item in data:
        if not item:
            continue
        flat = flatten_reference_fields(dict(item))
        for k, v in list(flat.items()):
            if isinstance(v, str) and v.strip() == "":
                flat[k] = None
        out.append(flat)
    return out


def parse_datetime(value: str) -> Optional[datetime]:  # deprecado
    """Tenta converter uma string para datetime testando vários formatos.

    Retorna um objeto datetime ou None se não conseguir parsear.
    Suporta formatos comuns encontrados no ServiceNow e na base de dados:
    - dd/mm/YYYY HH:MM:SS
    - dd/mm/YYYY HH:MM
    - YYYY-MM-DD HH:MM:SS
    - YYYY-MM-DDTHH:MM:SS[.ffffff]
    - ISO-like strings
    """
    if value is None:
        return None
    if not isinstance(value, str):
        return None
    v = value.strip()
    if v == "":
        return None

    fmts = (
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    )
    for fmt in fmts:
        try:
            return datetime.strptime(v, fmt)
        except Exception:
            continue

    # fallback para ISO via fromisoformat
    try:
        return datetime.fromisoformat(v)
    except Exception:
        return None


def coerce_dates_in_dict(d: dict) -> dict:  # deprecado
    return d


def normalize_date_columns(rows: List[Dict]) -> List[Dict]:  # deprecado
    return rows


def flatten_reference_fields(data: dict) -> dict:
    """Converte campos de referência do ServiceNow para valores simples"""
    for key in list(data.keys()):
        value = data.get(key)
        if isinstance(value, dict):
            possible_url = None
            for url_key in ("link", "url", "sys_href", "href"):
                u = value.get(url_key)
                if u and isinstance(u, str):
                    possible_url = u
                    break
            if not possible_url:
                for v in value.values():
                    if isinstance(v, str) and (
                        v.startswith("http://") or v.startswith("https://")
                    ):
                        possible_url = v
                        break

            if possible_url:
                try:
                    path = possible_url.split("?")[0]
                    path = path.rstrip("/")
                    id_part = path.split("/")[-1]
                    data[key] = id_part
                except Exception:
                    data[key] = str(possible_url)
            else:
                data[key] = value
    return data


def fetch_single_record(
    path: str, sys_id: str, params: Optional[Dict] = None, timeout: int = 30
) -> Optional[Dict]:
    """Busca um único registro no ServiceNow por `sys_id`.

    - `path` é o sufixo da URL da API (ex: 'api/now/table/sys_user' ou 'sys_user' se base_url já contempla o caminho).
    - Retorna o dicionário do registro ou `None` se não encontrado.

    Usa `get_servicenow_env()` para obter base_url, auth e headers.
    """
    params = dict(params or {})
    # sysparm_query limita por sys_id
    params.update({"sysparm_query": f"sys_id={sys_id}", "sysparm_limit": "1"})

    base_url, auth, headers = get_servicenow_env()

    # permite passar tanto 'sys_user' quanto caminhos completos. Normaliza para unir com base_url
    if path.startswith("http://") or path.startswith("https://"):
        url = path
    else:
        url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"

    resp = requests.get(
        url, auth=auth, headers=headers, params=params, timeout=timeout
    )
    if resp.status_code == 404:
        return None
    resp.raise_for_status()

    body = resp.json()
    result = body.get("result")
    if not result:
        return None
    if isinstance(result, list):
        return process_data([result[0]])[0]
    return process_data([result])[0]


@transaction.atomic
def upsert_by_sys_id(
    dataset: pl.DataFrame, model, log: Optional[Dict] = None
) -> None:
    """Upsert simples por sys_id. Todos os campos (exceto PK) tratados como texto; sem conversões de data.

    Se o modelo possuir campos etl_created_at/etl_updated_at (DateTimeField) o banco preenche via auto_now/auto_now_add.
    """
    if dataset is None:
        return
    if isinstance(dataset, pl.DataFrame):
        if dataset.is_empty():
            return
        rows = dataset.to_dicts()
    elif isinstance(dataset, list):
        rows = dataset
    else:
        try:
            rows = list(dataset)
        except Exception:
            rows = []
    if not rows:
        return

    field_names = {f.name for f in model._meta.fields}
    pk_name = model._meta.pk.name
    processed = []
    for r in rows:
        if not r:
            continue
        pr = {
            k: (v if v != "" else None)
            for k, v in r.items()
            if k in field_names
        }
        if pr.get("sys_id"):
            processed.append(pr)
    if not processed:
        return

    existing = {
        o.sys_id: o
        for o in model.objects.filter(
            sys_id__in=[r["sys_id"] for r in processed]
        )
    }
    to_create = []
    to_update = []
    for r in processed:
        sid = r["sys_id"]
        if sid in existing:
            obj = existing[sid]
            for k, v in r.items():
                if k not in (pk_name,):
                    setattr(obj, k, v)
            to_update.append(obj)
        else:
            to_create.append(model(**r))

    created = 0
    if to_create:
        created = len(model.objects.bulk_create(to_create, batch_size=1000))
    if to_update:
        update_fields = [
            f for f in field_names if f not in (pk_name, "sys_id")
        ]
        if update_fields:
            try:
                model.objects.bulk_update(
                    to_update, update_fields, batch_size=1000
                )
            except Exception:
                for obj in to_update:
                    try:
                        obj.save(update_fields=update_fields)
                    except Exception:
                        logging.exception(
                            "Falha update individual sys_id=%s",
                            getattr(obj, "sys_id", None),
                        )
    if isinstance(log, dict):
        log["n_inserted"] = log.get("n_inserted", 0) + created


# parse_datetime acima substitui a versão antiga/errada
