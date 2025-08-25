from django.db import models


class TaskLog(models.Model):
    """Armazena logs de execução de tasks/pipelines.

    Campos:
    - task_name: nome da classe/task executada
    - run_at: quando a task foi iniciada
    - log: conteúdo do log (JSON) gerado pela task
    """

    task_name = models.CharField(max_length=255)
    run_at = models.DateTimeField()
    # Use the framework JSONField for portability (Postgres or other backends)
    log = models.JSONField()

    def __str__(self):
        return f"{self.task_name} @ {self.run_at}"

    class Meta:
        db_table = "task_log"
        verbose_name = "Task Log"
        verbose_name_plural = "Task Logs"
