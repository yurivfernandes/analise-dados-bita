from datetime import datetime
from typing import Optional

from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Incident, IncidentNew


def parse_dt(value: Optional[str]) -> Optional[datetime]:
    """Parse a datetime string in format 'dd/mm/yyyy hh:mm:ss' or return None."""
    if not value:
        return None
    if isinstance(value, str):
        v = value.strip()
        if v == "":
            return None
        # tentar vários formatos possíveis (com e sem segundos)
        for fmt in ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M"):
            try:
                return datetime.strptime(v, fmt)
            except Exception:
                continue
    return None


class Command(BaseCommand):
    help = "Migra dados da tabela incident para incident_new convertendo campos de data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=1000,
            help="Tamanho do lote para processamento",
        )

    def handle(self, *args, **options):
        batch_size = options.get("batch_size") or 1000
        qs = Incident.objects.all()
        total = qs.count()
        self.stdout.write(f"Total registros em Incident: {total}")

        processed = 0
        with transaction.atomic():
            for start in range(0, total, batch_size):
                end = min(start + batch_size, total)
                subset = qs[start:end]
                for inc in subset:
                    data = {}
                    # copiar todos os campos simples (exceto id se houver)
                    for field in [f.name for f in Incident._meta.fields]:
                        if field == Incident._meta.pk.name:
                            continue
                        data[field] = getattr(inc, field)

                    # converter campos de data
                    data["opened_at"] = parse_dt(data.get("opened_at"))
                    data["closed_at"] = parse_dt(data.get("closed_at"))
                    data["resolved_at"] = parse_dt(data.get("resolved_at"))
                    data["u_fim_indisponibilidade"] = parse_dt(
                        data.get("u_fim_indisponibilidade")
                    )
                    data["u_data_normalizacao_servico"] = parse_dt(
                        data.get("u_data_normalizacao_servico")
                    )

                    # sys_id é PK em IncidentNew; garantir que exista
                    sys_id = getattr(inc, "sys_id", None)
                    if not sys_id:
                        self.stderr.write(
                            f"Pulando registro sem sys_id: {getattr(inc, 'number', None)}"
                        )
                        continue

                    # atualizar ou criar
                    IncidentNew.objects.update_or_create(
                        sys_id=sys_id, defaults=data
                    )
                    processed += 1
                self.stdout.write(f"Processados: {processed}/{total}")

        self.stdout.write(
            self.style.SUCCESS(f"Migração concluída. Total: {processed}")
        )
