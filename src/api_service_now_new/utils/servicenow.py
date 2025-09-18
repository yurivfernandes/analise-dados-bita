import logging
import os
from datetime import datetime

try:
    from dateutil import parser as _dateutil_parser  # type: ignore
except Exception:
    _dateutil_parser = None
from typing import Dict, List, Optional, Tuple

import polars as pl
import requests
from django.db import transaction
from django.db.models import DateTimeField


def get_servicenow_env() -> Tuple[str, tuple, Dict]:
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
    return base_url, (user, password), headers


def ensure_datetime(s: str, end: bool = False) -> str:
    """Garante timestamp completo quando recebido apenas a data (YYYY-MM-DD)."""
    if not isinstance(s, str):
        return s
    if len(s) == 10:
        return f"{s} 23:59:59" if end else f"{s} 00:00:00"
    return s


def paginate(
    path: str,
    params: Optional[Dict] = None,
    limit: int = 5000,
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

    # converte para polars DataFrame antes de retornar
    if not all_results:
        return pl.DataFrame()

    try:
        processed_results = []
        for result in all_results:
            # Processa campos de referência básicos
            processed_result = process_data([result])[0]

            # Adiciona timestamps ETL
            processed_result["etl_created_at"] = datetime.now()
            processed_result["etl_updated_at"] = datetime.now()

            processed_results.append(processed_result)
        # Normalizar colunas com mistura str/datetime e converter strings vazias em None
        try:
            processed_results = normalize_date_columns(processed_results)
        except Exception:
            pass
        return processed_results
    except (ValueError, TypeError) as e:
        logging.warning(
            "polars.DataFrame construction failed: %s; falling back", e
        )
        # fallback: construir DataFrame de forma mais permissiva
        return pl.DataFrame([dict(x) for x in all_results])


def process_data(data: List[Dict]) -> List[Dict]:
    """Processa os dados, aplicando flatten nos campos de referência"""
    processed_data = []

    for item in data:
        if not item:
            continue

        processed_item = flatten_reference_fields(item)
        # tentar converter strings que representam datas para datetime
        try:
            processed_item = coerce_dates_in_dict(processed_item)
        except Exception:
            # não falhar o pipeline por causa de parsing de datas
            pass
        # para garantir consistência quando construirmos DataFrames, converter
        # quaisquer datetime em strings ISO (o upsert converterá de volta)
        for k, v in list(processed_item.items()):
            if isinstance(v, datetime):
                processed_item[k] = v.isoformat(sep=" ")
        processed_data.append(processed_item)

    return processed_data


def parse_datetime(value: str) -> Optional[datetime]:
    """Tenta converter uma string para datetime usando dateutil se disponível

    Retorna objeto datetime ou None se não for possível.
    """
    if value is None or not isinstance(value, str):
        return None
    # service now frequentemente retorna 'YYYY-MM-DD HH:MM:SS' ou ISO com Z
    try:
        if _dateutil_parser:
            return _dateutil_parser.parse(value)
        # fallback simples: tentar fromisoformat (remove Z)
        v = value.replace("Z", "")
        return datetime.fromisoformat(v)
    except Exception:
        # tentar formatos comuns
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(value, fmt)
            except Exception:
                continue
    return None


def coerce_dates_in_dict(d: dict) -> dict:
    """Percorre o dict e converte valores que parecem datas para datetime.

    Regras:
    - se a chave contém 'sys_' ou termina com '_on' ou termina com '_at' tenta parse
    - se o valor é string e o parse for bem sucedido substitui pelo datetime
    """
    for k, v in list(d.items()):
        if isinstance(v, str):
            key = k.lower()
            if (
                "sys_" in key
                or key.endswith("_on")
                or key.endswith("_at")
                or key.endswith("_time")
                or key.startswith("last_")
            ):
                if v.strip() == "":
                    d[k] = None
                else:
                    pd = parse_datetime(v)
                    if pd is not None:
                        d[k] = pd
    return d


def _is_datetime_field(model, field_name: str) -> bool:
    try:
        f = next((f for f in model._meta.fields if f.name == field_name), None)
        return isinstance(f, DateTimeField)
    except Exception:
        return False


def normalize_date_columns(rows: List[Dict]) -> List[Dict]:
    """Se uma coluna tiver ao menos um datetime, converte strings daquela coluna em datetime.
    Também troca strings vazias por None em colunas de data.
    """
    if not rows:
        return rows
    keys = set().union(*(r.keys() for r in rows))
    for k in keys:
        has_dt = False
        has_str = False
        for r in rows:
            v = r.get(k)
            if isinstance(v, datetime):
                has_dt = True
            elif isinstance(v, str):
                has_str = True
        if has_dt and has_str:
            for r in rows:
                v = r.get(k)
                if isinstance(v, str):
                    if v.strip() == "":
                        r[k] = None
                    else:
                        pd = parse_datetime(v)
                        if pd is not None:
                            r[k] = pd
    return rows


def flatten_reference_fields(data: dict) -> dict:
    """Converte campos de referência do ServiceNow para valores simples"""
    for key in list(data.keys()):
        value = data.get(key)
        if isinstance(value, dict) and "value" in value:
            data[key] = value.get("value")
            data[f"dv_{key}"] = ""
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
    """Upsert em lote por `sys_id` para registros de `dataset` no `model`.

    Aceita `dataset` como `polars.DataFrame`, lista de dicts ou qualquer iterável de dicts.
    Atualiza em transação usando `bulk_create` e `bulk_update`.
    Atualiza `log["n_inserted"]` e `log["n_updated"]` quando informado.
    """
    # Converte para lista de dicionários
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

    # coletar nomes de campos válidos do model
    model_field_names = {f.name for f in model._meta.fields}
    pk_name = model._meta.pk.name

    # filtrar rows para conter apenas campos do model
    processed = []
    for r in rows:
        if not r:
            continue
        pr = {k: v for k, v in r.items() if k in model_field_names}
        if pr and pr.get("sys_id"):
            processed.append(pr)

    if not processed:
        return

    sys_ids = [r["sys_id"] for r in processed]

    # buscar existentes em batch
    existing_qs = model.objects.filter(sys_id__in=sys_ids)
    existing_map = {getattr(obj, "sys_id"): obj for obj in existing_qs}

    to_create = []
    to_update = []

    for row in processed:
        sid = row["sys_id"]
        if sid in existing_map:
            obj = existing_map[sid]
            for k, v in row.items():
                setattr(obj, k, v)
            to_update.append(obj)
        else:
            to_create.append(model(**row))

    n_created = 0

    if to_create:
        created_objs = model.objects.bulk_create(to_create, batch_size=1000)
        n_created = len(created_objs)

    if to_update:
        # campos a atualizar: todos os campos do model exceto pk e sys_id
        update_fields = [
            f for f in model_field_names if f not in (pk_name, "sys_id")
        ]
        if update_fields:
            model.objects.bulk_update(
                to_update, update_fields, batch_size=1000
            )

    if isinstance(log, dict):
        log["n_inserted"] = log.get("n_inserted", 0) + n_created
