from datetime import datetime
import logging
import os
from typing import Any, Dict, List, Optional, Tuple

import polars as pl
import requests


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
        processed_data.append(processed_item)

    return processed_data


def flatten_reference_fields(data: dict) -> dict:
    """Converte campos de referência do ServiceNow para valores simples"""
    for key in list(data.keys()):
        value = data.get(key)
        if isinstance(value, dict) and "value" in value:
            data[key] = value.get("value")
            data[f"dv_{key}"] = ""
    return data
