# Django Models: Documentação Detalhada

## O que são Models?

Models são a representação das tabelas do banco de dados em código Python. Eles são a fonte única de informação sobre seus dados e contêm os campos e comportamentos essenciais dos dados armazenados.

## Paralelo com SQL Server

| Django Model | SQL Server |
|-------------|------------|
| Classe Model | Tabela |
| Atributo de classe | Coluna |
| Instância de Model | Linha/Registro |
| Manager (objects) | Stored Procedures |
| QuerySet | Resultado de SELECT |

## Estrutura Básica

```python
from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'clientes'
        ordering = ['-criado_em']
```

SQL Server equivalente:
```sql
CREATE TABLE clientes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(100) NOT NULL,
    email NVARCHAR(254) UNIQUE NOT NULL,
    criado_em DATETIME DEFAULT GETDATE()
)
```

## Tipos de Dados e Comparações com SQL Server

### Campos de Texto
| Django | SQL Server | Descrição |
|--------|------------|-----------|
| CharField | VARCHAR/NVARCHAR | Texto com tamanho máximo |
| TextField | TEXT/NTEXT | Texto sem limite de tamanho |
| EmailField | VARCHAR + validação | Email com validação |
| URLField | VARCHAR + validação | URL com validação |

### Campos Numéricos
| Django | SQL Server | Descrição |
|--------|------------|-----------|
| IntegerField | INT | Números inteiros |
| BigIntegerField | BIGINT | Inteiros grandes |
| DecimalField | DECIMAL | Números decimais precisos |
| FloatField | FLOAT | Números decimais |

### Campos de Data/Hora
| Django | SQL Server | Descrição |
|--------|------------|-----------|
| DateField | DATE | Apenas data |
| TimeField | TIME | Apenas hora |
| DateTimeField | DATETIME | Data e hora |

## Exemplos Práticos

### 1. Model com Diferentes Tipos de Campos
```python
from django.db import models

class Produto(models.Model):
    # Campos de texto
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    sku = models.CharField(max_length=20, unique=True)
    
    # Campos numéricos
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    peso = models.FloatField(null=True, blank=True)
    
    # Campos de data/hora
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    data_validade = models.DateField(null=True)
    
    # Campos booleanos e escolhas
    ativo = models.BooleanField(default=True)
    categoria = models.CharField(
        max_length=20,
        choices=[
            ('ALIMENTO', 'Alimento'),
            ('BEBIDA', 'Bebida'),
            ('LIMPEZA', 'Limpeza')
        ]
    )
    
    class Meta:
        db_table = 'produtos'
        indexes = [
            models.Index(fields=['nome']),
            models.Index(fields=['sku']),
        ]
```

SQL Server equivalente:
```sql
CREATE TABLE produtos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nome NVARCHAR(100) NOT NULL,
    descricao NTEXT,
    sku NVARCHAR(20) UNIQUE NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    estoque INT DEFAULT 0 NOT NULL,
    peso FLOAT NULL,
    criado_em DATETIME DEFAULT GETDATE() NOT NULL,
    atualizado_em DATETIME NOT NULL,
    data_validade DATE NULL,
    ativo BIT DEFAULT 1 NOT NULL,
    categoria NVARCHAR(20) CHECK (categoria IN ('ALIMENTO', 'BEBIDA', 'LIMPEZA')) NOT NULL
);

CREATE INDEX IX_produtos_nome ON produtos(nome);
CREATE INDEX IX_produtos_sku ON produtos(sku);
```

### 2. Relacionamentos

#### One-to-Many (1:N)
```python
class Pedido(models.Model):
    cliente = models.ForeignKey(
        'Cliente',
        on_delete=models.CASCADE,
        related_name='pedidos'
    )
    # ...outros campos
```

SQL Server:
```sql
CREATE TABLE pedidos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    cliente_id INT NOT NULL,
    -- ...outros campos
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
```

#### Many-to-Many (N:N)
```python
class Produto(models.Model):
    categorias = models.ManyToManyField('Categoria', through='ProdutoCategoria')

class ProdutoCategoria(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    data_adicao = models.DateTimeField(auto_now_add=True)
```

SQL Server:
```sql
CREATE TABLE produto_categoria (
    produto_id INT,
    categoria_id INT,
    data_adicao DATETIME DEFAULT GETDATE(),
    PRIMARY KEY (produto_id, categoria_id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);
```

## Operações Comuns

### Inserção
```python
# Django
produto = Produto.objects.create(
    nome="Refrigerante",
    preco=5.99,
    categoria="BEBIDA"
)

# SQL Server
INSERT INTO produtos (nome, preco, categoria)
VALUES ('Refrigerante', 5.99, 'BEBIDA');
```

### Consultas
```python
# Django - Filtros básicos
produtos = Produto.objects.filter(
    preco__lt=10.00,
    categoria="BEBIDA",
    ativo=True
)

# SQL Server
SELECT * FROM produtos
WHERE preco < 10.00
AND categoria = 'BEBIDA'
AND ativo = 1;

# Django - Joins
pedidos = Pedido.objects.select_related('cliente').filter(
    cliente__cidade="São Paulo"
)

# SQL Server
SELECT p.* FROM pedidos p
INNER JOIN clientes c ON p.cliente_id = c.id
WHERE c.cidade = 'São Paulo';
```

## Boas Práticas e Dicas

1. **Validação de Campos**
```python
class Produto(models.Model):
    def clean(self):
        if self.preco < 0:
            raise ValidationError("Preço não pode ser negativo")
```

2. **Índices Corretos**
```python
class Meta:
    indexes = [
        models.Index(fields=['nome']),
        models.Index(fields=['criado_em', 'categoria']),
    ]
```

3. **Campos Calculados**
```python
from django.db.models import F

class Pedido(models.Model):
    @property
    def total_com_desconto(self):
        return F('total') - F('desconto')
```

4. **Managers Customizados**
```python
class AtivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(ativo=True)

class Produto(models.Model):
    objects = models.Manager()
    ativos = AtivoManager()
```

5. **Sinais para Automatização**
```python
@receiver(post_save, sender=Pedido)
def atualiza_estoque(sender, instance, created, **kwargs):
    if created:
        instance.produto.reduzir_estoque(instance.quantidade)
```

## Performance e Otimização

1. **Select Related para FKs**
```python
# Bom - Uma query
pedidos = Pedido.objects.select_related('cliente').all()

# Ruim - N+1 queries
pedidos = Pedido.objects.all()
for pedido in pedidos:
    print(pedido.cliente.nome)  # Nova query para cada pedido
```

2. **Prefetch Related para M2M**
```python
produtos = Produto.objects.prefetch_related('categorias').all()
```

3. **Bulk Operations**
```python
# Criar múltiplos
Produto.objects.bulk_create([
    Produto(nome="Item 1"),
    Produto(nome="Item 2"),
])

# Atualizar múltiplos
Produto.objects.filter(categoria="BEBIDA").update(preco=F('preco') * 1.1)
```

## Recursos Avançados

1. **Constraints**
```python
class Meta:
    constraints = [
        models.CheckConstraint(
            check=models.Q(idade__gte=18),
            name='idade_maior_18'
        ),
        models.UniqueConstraint(
            fields=['cpf'],
            name='cpf_unico'
        )
    ]
```

2. **Herança de Models**
```python
class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    
class Cliente(Pessoa):
    codigo = models.CharField(max_length=20)
```

Consulte a documentação específica de cada app para ver exemplos práticos de implementação no projeto.
