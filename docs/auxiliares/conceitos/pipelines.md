# Django Pipelines

## O que são Pipelines?

Pipelines no Django são uma série de operações sequenciais que processam dados de forma estruturada. São comumente usados para:
- ETL (Extract, Transform, Load)
- Processamento em lote
- Transformação de dados
- Sincronização entre sistemas

## Estrutura Básica

```python
from django.db import transaction

class BasePipeline:
    def __init__(self):
        self.log = {
            'started_at': None,
            'finished_at': None,
            'n_processed': 0,
            'n_errors': 0
        }

    def extract(self):
        """Extrai dados da fonte"""
        raise NotImplementedError

    def transform(self):
        """Transforma os dados"""
        raise NotImplementedError

    def load(self):
        """Carrega dados no destino"""
        raise NotImplementedError

    @transaction.atomic
    def run(self):
        """Executa o pipeline"""
        try:
            self.extract()
            self.transform()
            self.load()
            return self.log
        except Exception as e:
            self.log['error'] = str(e)
            raise
```

## Exemplos Práticos

### Pipeline de Análise

```python
from django.db.models import Count, Avg, Sum, F

class AnalyticsPipeline(BasePipeline):
    def run(self):
        return Pedido.objects.values('produto__categoria').annotate(
            total_vendas=Count('id'),
            valor_medio=Avg('total'),
            lucro=Sum(F('total') - F('custo'))
        ).order_by('-total_vendas')
```

### Pipeline de ETL

```python
class ETLPipeline(BasePipeline):
    def extract(self):
        self.dados = FonteExterna.objects.filter(
            processado=False
        ).values()

    def transform(self):
        self.transformed = []
        for dado in self.dados:
            self.transformed.append({
                'id': dado['id_externo'],
                'valor': float(dado['valor']) * 1.1,
                'data': dado['data'].date()
            })

    @transaction.atomic
    def load(self):
        for item in self.transformed:
            Destino.objects.create(**item)
            self.log['n_processed'] += 1
```

## Boas Práticas

1. **Atomicidade**
```python
@transaction.atomic
def load(self):
    """Garante que todas as operações sejam atômicas"""
    # ...existing code...
```

2. **Logging**
```python
def run(self):
    self.log['started_at'] = timezone.now()
    try:
        # ...existing code...
    finally:
        self.log['finished_at'] = timezone.now()
```

3. **Processamento em Lotes**
```python
def load(self):
    Destino.objects.bulk_create(
        self.transformed,
        batch_size=1000
    )
```

## Implementação no Projeto

Para implementações específicas, consulte:
- `app.utils.pipeline` para a classe base
- `dw_analytics.pipelines` para pipelines de análise
- `power_bi.tasks` para pipelines de integração

## Dicas de Performance

1. Utilize `select_related()` e `prefetch_related()` para queries otimizadas
2. Implemente processamento em lotes para grandes volumes
3. Use cache para resultados frequentemente acessados
4. Considere async/await para operações I/O bound

## Monitoramento

```python
class MonitoredPipeline(BasePipeline):
    def __init__(self):
        super().__init__()
        self.start_time = None

    def run(self):
        self.start_time = timezone.now()
        try:
            return super().run()
        finally:
            self.log.update({
                'duration': (timezone.now() - self.start_time).total_seconds(),
                'memory_usage': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            })
```
```

## Monitoramento e Logs

### Exemplo de Log
```python
{
    'n_inserted': 1500,
    'n_deleted': 100,
    'started_at': '2024-02-20 10:00:00',
    'finished_at': '2024-02-20 10:05:00',
    'duration': 300.0  # segundos
}
```

### Comparação com SQL Server
- Logs Django: Dicionário Python
- SQL Server: Tabela sys.dm_exec_requests

## Casos de Uso

1. **Carga Periódica**
   - Importação noturna
   - Atualização de métricas
   - Geração de relatórios

2. **Processamento Sob Demanda**
   - Exportações grandes
   - Recálculo de dados
   - Correções em lote

3. **Integração entre Sistemas**
   - Sincronização de bases
   - Migração de dados
   - Consolidação de fontes

## Dicas de Performance

1. **Processamento em Lotes**
```python
def load(self):
    # Bulk create - mais eficiente
    Destino.objects.bulk_create(
        self.transformed_data,
        batch_size=1000
    )
```

2. **Otimização de Memória**
```python
def extract(self):
    # Processa em chunks para grandes volumes
    for chunk in pd.read_csv('big_file.csv', chunksize=10000):
        self._process_chunk(chunk)
```

3. **Paralelização**
```python
from concurrent.futures import ThreadPoolExecutor

def transform(self):
    with ThreadPoolExecutor() as executor:
        # Processa múltiplos chunks em paralelo
        futures = [executor.submit(self._transform_chunk, chunk)
                  for chunk in self.chunks]
```

## Considerações Finais

- Pipelines são essenciais para processamento em lote
- Combine com Celery para execução assíncrona
- Mantenha logs detalhados para debug
- Use transações para garantir consistência
- Otimize para grandes volumes de dados

Consulte o código fonte de `app.utils.pipeline` para mais detalhes de implementação.
