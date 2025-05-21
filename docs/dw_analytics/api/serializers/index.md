# Serializers

## O que são serializers?

Serializers são componentes do Django REST Framework responsáveis por converter objetos Python/Django (geralmente modelos) em formatos que podem ser enviados via API (como JSON) e vice-versa.

---

## Para que servem?

- **Serializar**: Transformar objetos do banco de dados em JSON para resposta de API.
- **Desserializar**: Validar e transformar dados recebidos (JSON) em objetos Python/modelos.
- **Validação**: Garantir que os dados recebidos estão corretos antes de salvar no banco.

---

## Exemplo básico de utilização

```python
from rest_framework import serializers
from .models import FIncidentsBita

class FIncidentsBitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIncidentsBita
        fields = "__all__"
```

- O serializer acima converte todos os campos do modelo `FIncidentsBita` para JSON e valida dados recebidos para criação/atualização.

---

## Exemplos avançados de serializers

### 1. Serializer com campos calculados (concatenação, agregação, etc.)

```python
from rest_framework import serializers
from .models import FIncidentsBita

class FIncidentsBitaCustomSerializer(serializers.ModelSerializer):
    descricao_completa = serializers.SerializerMethodField()

    class Meta:
        model = FIncidentsBita
        fields = ["id", "number", "assignment_group", "descricao_completa"]

    def get_descricao_completa(self, obj):
        # Exemplo: concatena dois campos do model
        return f"{obj.number} - {obj.assignment_group}"
```
- `descricao_completa` é um campo novo, criado a partir de outros campos do modelo.

---

### 2. Serializer retornando apenas campos específicos

```python
from rest_framework import serializers
from .models import FIncidentsBita

class FIncidentsBitaResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIncidentsBita
        fields = ["id", "number", "assignment_group"]
```
- Apenas os campos listados em `fields` serão retornados na resposta da API.

---

### 3. Serializer com validação customizada

```python
from rest_framework import serializers
from .models import FIncidentsBita

class FIncidentsBitaValidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FIncidentsBita
        fields = "__all__"

    def validate_number(self, value):
        if not value.startswith("INC"):
            raise serializers.ValidationError("O número deve começar com 'INC'")
        return value
```
- O método `validate_<campo>` permite validar valores de campos específicos.

---

## Por que utilizar serializers?

- Padronizam a comunicação entre backend e frontend.
- Permitem validação automática dos dados.
- Facilitam a customização de campos e regras de negócio.
- Tornam o código mais seguro e robusto.

---

## Como usar

- Crie um serializer para cada modelo que será exposto via API.
- Use o serializer nas views para transformar dados de entrada e saída.
- Pode customizar métodos de validação ou campos conforme necessário.

---

## Exemplo prático em uma view

```python
from rest_framework.viewsets import ModelViewSet
from .models import FIncidentsBita
from .serializers import FIncidentsBitaSerializer

class FIncidentsBitaViewset(ModelViewSet):
    queryset = FIncidentsBita.objects.all()
    serializer_class = FIncidentsBitaSerializer
```

---

Consulte os arquivos individuais para detalhes de cada serializer.
