import polars as pl

# from celery import shared_task
from django.db import models, transaction
from django.utils import timezone


class Pipeline:
    """Classe padrão que generaliza os métodos de todas as Pipelines de dados"""

    def __init__(self, **kwargs):
        self.log = {
            "n_inserted": 0,
            "n_deleted": 0,
            "started_at": timezone.now(),
            "finished_at": None,
            "duration": None,
        }

    def __enter__(self):  ###IMPLEMENTAR O SAVE DOS LOGS.
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.log["finished_at"] = timezone.now()
        self.log["duration"] = round(
            (self.log["finished_at"] - self.log["started_at"]).total_seconds(),
            2,
        )

    def run(self) -> dict:
        """Implementar o método run que executa a task retornando um Dicionário"""
        raise NotImplementedError("Subclass must implement this method")

    def transform_dataset(self) -> None:
        """Implementar o método transform_dataset irá fazer o fluxo de transformação do dataset, utilizando os métodos disponíveis nos mixins."""
        raise NotImplementedError("Subclass must implement this method")

    @transaction.atomic
    def load(
        self, dataset: pl.DataFrame, model: models.Model, filtro: dict
    ) -> None:
        """
        Executa a carga de dados no banco de dados de forma transacional.

        Este método garante a integridade dos dados ao realizar a exclusão e inserção
        dentro de uma transação atômica. Caso ocorra algum erro durante o processo,
        um rollback será executado, garantindo que nenhuma alteração parcial seja
        aplicada ao banco de dados.

        Operações realizadas:
        1. **DELETE**: Remove registros do banco de dados com base no filtro fornecido.
        - O filtro deve ser um dicionário (`dict`).
        - Se o filtro estiver vazio, todos os registros da tabela serão excluídos.
        - Para excluir registros específicos, basta fornecer um dicionário com
            chave(s) e valor(es) correspondentes às colunas desejadas.

        2. **SAVE**: Insere novos registros no banco de dados conforme os dados
        presentes no `dataset` e o modelo (`model`) especificado.

        Parâmetros:
        - `dataset` (`pl.DataFrame`): Conjunto de dados a ser inserido no banco.
        - `model` (`models.Model`): Modelo Django que representa a tabela onde os
        dados serão manipulados.
        - `filtro` (`dict`): Critérios para exclusão de registros antes da inserção.

        """

        # medir tempo do load completo
        started = timezone.now()
        self._delete(filtro=filtro, model=model)
        self._save(dataset=dataset, model=model)
        finished = timezone.now()
        load_duration = round((finished - started).total_seconds(), 2)
        self.log["load_duration"] = load_duration
        print(f"...LOAD DURATION: {load_duration}s (delete+save)...")

    def _delete(self, filtro: dict, model=models.Model) -> None:
        """Deleta os registros na base, conforme o model e o filtro selecionado."""
        print(
            f"...LIMPANDO OS DADOS DO MODEL [{model.__name__}] NO BANCO DE DADOS ..."
        )
        print(f"....FILTROS UTILIZADOS: {filtro}...")
        started = timezone.now()
        n_deleted, __ = model.objects.filter(**filtro).delete()
        finished = timezone.now()
        duration = round((finished - started).total_seconds(), 2)
        self.log["n_deleted"] = n_deleted
        self.log["delete_duration"] = duration
        print(f"...{n_deleted} DADOS DELETADOS NO BANCO DE DADOS...")
        print(f"...DELETE DURATION: {duration}s...")

    def _save(self, dataset: pl.DataFrame, model=models.Model) -> None:
        """Salva os dados no banco de dados no model selecionado."""
        print(
            f"...SALVANDO OS DADOS NO BANCO DE DADOS NO MODEL: [{model.__name__}]..."
        )
        if dataset.is_empty():
            print("...DATASET VAZIO: nada a salvar...")
            self.log.setdefault("save_duration", 0.0)
            return
        started = timezone.now()
        objs = [model(**vals) for vals in dataset.to_dicts()]
        bulk = model.objects.bulk_create(objs=objs, batch_size=1000)
        finished = timezone.now()
        duration = round((finished - started).total_seconds(), 2)
        self.log["n_inserted"] = len(bulk)
        self.log["save_duration"] = duration
        print(f"...{len(bulk)} REGISTROS SALVOS NO BANCO DE DADOS...")
        print(f"...SAVE DURATION: {duration}s...")
