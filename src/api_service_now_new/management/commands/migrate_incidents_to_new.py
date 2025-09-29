from typing import List

import polars as pl
from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import Incident, IncidentNew
from ...utils.servicenow import parse_datetime


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

        # carregar todos os Incident em memória como lista de dicts
        qs = Incident.objects.all()
        total = qs.count()
        self.stdout.write(f"Total registros em Incident: {total}")

        # construir lista de dicts com todos os campos
        rows: List[dict] = []
        field_names = [f.name for f in Incident._meta.fields]
        pk_name = Incident._meta.pk.name
        for obj in qs:
            d = {f: getattr(obj, f) for f in field_names if f != pk_name}
            # incluir sys_id também (pode ser pk em Incident)
            if hasattr(obj, "sys_id"):
                d["sys_id"] = getattr(obj, "sys_id")
            rows.append(d)

        if not rows:
            self.stdout.write(
                self.style.WARNING("Nenhum registro encontrado.")
            )
            return

        # criar DataFrame polars
        df = pl.DataFrame(rows)

        # colunas de data a normalizar
        date_cols = [
            "opened_at",
            "closed_at",
            "resolved_at",
            "u_fim_indisponibilidade",
            "u_data_normalizacao_servico",
        ]

        # usar map_elements com a função parse_datetime já existente (mais rápido que apply)
        for c in date_cols:
            if c in df.columns:
                df = df.with_column(
                    pl.col(c)
                    .map_elements(parse_datetime, return_dtype=pl.Datetime)
                    .alias(c)
                )

        # persistir: iterar e fazer update_or_create
        processed = 0
        with transaction.atomic():
            for row in df.to_dicts():
                sys_id = row.get("sys_id")
                if not sys_id:
                    self.stderr.write(
                        f"Pulando linha sem sys_id: {row.get('number')!r}"
                    )
                    continue

                # somente campos que existem em IncidentNew
                valid_fields = {f.name for f in IncidentNew._meta.fields}
                defaults = {
                    k: v
                    for k, v in row.items()
                    if k in valid_fields and k != pk_name
                }

                IncidentNew.objects.update_or_create(
                    sys_id=sys_id, defaults=defaults
                )
                processed += 1

                if processed % batch_size == 0:
                    self.stdout.write(f"Processados: {processed}/{total}")

        self.stdout.write(
            self.style.SUCCESS(f"Migração concluída. Total: {processed}")
        )
