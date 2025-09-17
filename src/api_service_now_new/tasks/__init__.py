"""Tasks package for api_service_now_new module."""

from .load_incidents_opened import LoadIncidentsOpened
from .load_incidents_updated import LoadIncidentsUpdated

__all__ = [
    "LoadIncidentsOpened",
    "LoadIncidentsUpdated",
]
