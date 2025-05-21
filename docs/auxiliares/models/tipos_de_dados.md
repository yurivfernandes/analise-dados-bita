# Tipos de Dados em Models Django

Esta página apresenta os principais tipos de campos que podem ser usados em models Django, exemplos de uso e o paralelo com tipos SQL.

---

## Tipos de campos e paralelos com SQL

- **CharField**  
  Django:  
  ```python
  nome = models.CharField(max_length=100)
  ```  
  SQL:  
  ```sql
  nome VARCHAR(100)
  ```
  Usado para textos curtos, nomes, códigos.

- **TextField**  
  Django:  
  ```python
  descricao = models.TextField()
  ```  
  SQL:  
  ```sql
  descricao TEXT
  ```
  Usado para textos longos, descrições.

- **IntegerField**  
  Django:  
  ```python
  idade = models.IntegerField()
  ```  
  SQL:  
  ```sql
  idade INTEGER
  ```
  Usado para números inteiros.

- **FloatField**  
  Django:  
  ```python
  nota = models.FloatField()
  ```  
  SQL:  
  ```sql
  nota FLOAT
  ```
  Usado para números decimais de precisão dupla.

- **DecimalField**  
  Django:  
  ```python
  preco = models.DecimalField(max_digits=10, decimal_places=2)
  ```  
  SQL:  
  ```sql
  preco DECIMAL(10,2)
  ```
  Usado para valores monetários ou decimais precisos.

- **BooleanField**  
  Django:  
  ```python
  ativo = models.BooleanField()
  ```  
  SQL:  
  ```sql
  ativo BOOLEAN
  ```
  Usado para valores verdadeiro/falso.

- **DateField**  
  Django:  
  ```python
  data_nascimento = models.DateField()
  ```  
  SQL:  
  ```sql
  data_nascimento DATE
  ```
  Usado para datas (sem hora).

- **DateTimeField**  
  Django:  
  ```python
  criado_em = models.DateTimeField(auto_now_add=True)
  ```  
  SQL:  
  ```sql
  criado_em DATETIME
  ```
  Usado para data e hora.

- **TimeField**  
  Django:  
  ```python
  horario = models.TimeField()
  ```  
  SQL:  
  ```sql
  horario TIME
  ```
  Usado para horários.

- **EmailField**  
  Django:  
  ```python
  email = models.EmailField()
  ```  
  SQL:  
  ```sql
  email VARCHAR(254)
  ```
  Usado para e-mails, com validação automática.

- **URLField**  
  Django:  
  ```python
  site = models.URLField()
  ```  
  SQL:  
  ```sql
  site VARCHAR(200)
  ```
  Usado para URLs, com validação automática.

- **AutoField**  
  Django:  
  ```python
  id = models.AutoField(primary_key=True)
  ```  
  SQL:  
  ```sql
  id SERIAL PRIMARY KEY
  ```
  Usado para IDs auto-incrementais.

- **BigAutoField**  
  Django:  
  ```python
  id = models.BigAutoField(primary_key=True)
  ```  
  SQL:  
  ```sql
  id BIGSERIAL PRIMARY KEY
  ```
  Usado para IDs auto-incrementais grandes.

- **ForeignKey**  
  Django:  
  ```python
  cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
  ```  
  SQL:  
  ```sql
  cliente_id INTEGER REFERENCES cliente(id)
  ```
  Relacionamento muitos-para-um.

- **ManyToManyField**  
  Django:  
  ```python
  grupos = models.ManyToManyField(Grupo)
  ```  
  SQL:  
  ```sql
  -- Cria uma tabela associativa entre as tabelas relacionadas
  ```
  Relacionamento muitos-para-muitos.

- **OneToOneField**  
  Django:  
  ```python
  perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
  ```  
  SQL:  
  ```sql
  perfil_id INTEGER UNIQUE REFERENCES perfil(id)
  ```
  Relacionamento um-para-um.

- **FileField / ImageField**  
  Django:  
  ```python
  arquivo = models.FileField(upload_to='uploads/')
  foto = models.ImageField(upload_to='fotos/')
  ```  
  SQL:  
  ```sql
  arquivo VARCHAR(100)
  foto VARCHAR(100)
  ```
  Usado para armazenar o caminho do arquivo/imagem.

---

> Estes são os tipos mais comuns. Consulte a [documentação oficial do Django](https://docs.djangoproject.com/pt-br/stable/ref/models/fields/) para mais opções e detalhes.
