from typing import Optional

from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_GET

from .tasks import (
	LoadNode,
	load_node_async,
	LoadInterface,
	load_interface_async,
	LoadCustomPollerAssignment,
	load_custom_poller_assignment_async,
	LoadCapacityDatacenter,
	load_capacity_datacenter_async,
	LoadCustompollerStatistics,
	load_custom_poller_statistics_async,
)


@require_GET
def run_capacity_workflow(request: HttpRequest) -> JsonResponse:
	"""Roda o workflow completo de carga.

	Query params:
	- days_back: int (opcional) — repassado para as tasks que aceitam esse parâmetro
	- async: 'true' para disparar as tasks assíncronas via Celery (opcional)

	Fluxo: node -> interface -> custom poller assignment -> response_time -> custom poller statistics
	"""
	days_back: Optional[str] = request.GET.get("days_back")
	async_mode = request.GET.get("async", "false").lower() == "true"

	results = {}

	# 1) Nodes
	if async_mode:
		load_node_async.apply_async()
		results["node"] = "dispatched"
	else:
		loader = LoadNode()
		loader.run()
		results["node"] = "done"

	# 2) Interface
	if async_mode:
		load_interface_async.apply_async()
		results["interface"] = "dispatched"
	else:
		loader = LoadInterface()
		loader.run()
		results["interface"] = "done"

	# 3) Custom Poller Assignment
	if async_mode:
		load_custom_poller_assignment_async.apply_async()
		results["custom_poller_assignment"] = "dispatched"
	else:
		loader = LoadCustomPollerAssignment()
		loader.run()
		results["custom_poller_assignment"] = "done"

	# 4) Response Time (accepts days_back)
	if async_mode:
		if days_back is not None:
			load_capacity_datacenter_async.apply_async(args=(None,), kwargs={"days_back": int(days_back)})
		else:
			load_capacity_datacenter_async.apply_async()
		results["response_time"] = "dispatched"
	else:
		loader = LoadCapacityDatacenter(days_back=int(days_back) if days_back is not None else None)
		loader.run()
		results["response_time"] = "done"

	# 5) Custom Poller Statistics (accepts days_back)
	if async_mode:
		if days_back is not None:
			load_custom_poller_statistics_async.apply_async(args=(None,), kwargs={"days_back": int(days_back)})
		else:
			load_custom_poller_statistics_async.apply_async()
		results["custom_poller_statistics"] = "dispatched"
	else:
		loader = LoadCustompollerStatistics(days_back=int(days_back) if days_back is not None else None)
		loader.run()
		results["custom_poller_statistics"] = "done"

	return JsonResponse({"status": "ok", "results": results})
