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
        qs = Incident.objects.all()
        field_names = [f.name for f in Incident._meta.fields]
        total = qs.count()
        self.stdout.write(f"Total registros em Incident: {total}")

        # trazer exatamente os campos do model como dicts (melhor performance)
        rows = list(qs.values(*field_names))
        df = pl.DataFrame(data=rows)
        # inicializar log
        self.log = {}

        date_cols = [
            "opened_at",
            "closed_at",
            "resolved_at",
            "u_fim_indisponibilidade",
            "u_data_normalizacao_servico",
        ]
        self.stdout.write("Dataframe criado, normalizando as colunas...")
        # usar map_elements com a função parse_datetime já existente (mais rápido que apply)
        for c in date_cols:
            if c in df.columns:
                self.stdout.write(f"Normalizando a coluna: {c}")
                df = df.with_columns(
                    pl.col(c)
                    .map_elements(parse_datetime, return_dtype=pl.Datetime)
                    .alias(c)
                )
        self.stdout.write("Dataframe normalizado...")
        self._save(dataset=df, model=IncidentNew)

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
