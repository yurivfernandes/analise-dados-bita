import polars as pl

# from celery import shared_task
from django.db import models, transaction

from .mixin_get_dataset_solar import MixinGetDatasetSolar


class MixinTasks(MixinGetDatasetSolar):
    """Classe que define os métodos e estrutura principal das tasks"""

    def run(self) -> dict:
        """Implementar o método run que executa a task retornando um Dicionário"""
        raise NotImplementedError("Subclass must implement this method")

    @transaction.atomic
    def load(self, dataset: pl.DataFrame, model: models.Model) -> None:
        """Método que controla o save e o delete dos registros através de uma transação atomica, garantindo que os dados serão salvos ou o rollback acontece."""
        self.log["n_deleted"] = self.delete(model=model)
        self.log["n_inserted"] = self.save(dataset=dataset, model=model)

    def delete(self, model=models.Model) -> int:
        print("...LIMPANDO A BASE NO BANCO DE DADOS...")
        n_deleted, __ = model.objects.filter(**self._filtro).delete()
        return n_deleted

    def save(self, dataset: pl.DataFrame, model=models.Model) -> int:
        """Salva os dados no banco de dados no model selecionado."""
        print("...SALVANDO OS DADOS NO BANCO DE DADOS...")
        if dataset.is_empty():
            return

        objs = [model(**vals) for vals in dataset.to_dicts()]
        bulk = model.objects.using("power_bi").bulk_create(
            objs=objs, batch_size=1000
        )
        return len(bulk)
