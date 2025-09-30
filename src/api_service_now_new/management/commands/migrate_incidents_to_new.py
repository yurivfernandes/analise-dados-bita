from typing import List

import polars as pl
from django.core.management.base import BaseCommand
from django.db import models, transaction
from django.utils import timezone

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
        CHUNK_SIZE = 10_000
        qs_base = Incident.objects.all().order_by("sys_id")

        total = qs_base.count()

        field_names = [f.name for f in Incident._meta.fields if f.name != "id"]
        self.log = {}

        for offset in range(0, total, CHUNK_SIZE):
            self.stdout.write(
                f"Processando registros {offset} até {offset + CHUNK_SIZE}..."
            )

            qs_chunk = qs_base[offset : offset + CHUNK_SIZE].values(
                *field_names
            )
            raw_data = list(qs_chunk.values(*field_names))
            clean_data = [
                {k: str(v) if v is not None else None for k, v in row.items()}
                for row in raw_data
            ]

            df = pl.DataFrame(
                list(clean_data),
                schema={f: pl.String for f in field_names},
                infer_schema_length=CHUNK_SIZE,
            )

            date_cols = [
                "opened_at",
                "closed_at",
                "resolved_at",
                "u_fim_indisponibilidade",
                "u_data_normalizacao_servico",
            ]
            for c in date_cols:
                if c in df.columns:
                    self.stdout.write(f"Normalizando a coluna: {c}")
                    df = df.with_columns(
                        pl.col(c)
                        .map_elements(parse_datetime, return_dtype=pl.Datetime)
                        .alias(c)
                    )

            self._save(dataset=df, model=IncidentNew)

        self.stdout.write("Todos os blocos foram processados e salvos.")

    def _save(self, dataset: pl.DataFrame, model=models.Model) -> None:
        """Salva os dados no banco de dados no model selecionado."""
        self.stdout.write(
            f"...SALVANDO OS DADOS NO BANCO DE DADOS NO MODEL: [{model.__name__}]..."
        )
        if dataset.is_empty():
            self.stdout.write("...DATASET VAZIO: nada a salvar...")
            self.log.setdefault("save_duration", 0.0)
            return
        started = timezone.now()
        objs = [model(**vals) for vals in dataset.to_dicts()]
        bulk = model.objects.bulk_create(objs, batch_size=1000)
        finished = timezone.now()
        duration = round((finished - started).total_seconds(), 2)
        self.log["n_inserted"] = len(bulk)
        self.log["save_duration"] = duration
        self.stdout.write(
            f"...{len(bulk)} REGISTROS SALVOS NO BANCO DE DADOS..."
        )
        self.stdout.write(f"...SAVE DURATION: {duration}s...")
