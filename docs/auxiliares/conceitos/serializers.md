# Django REST Framework Serializers

## O que são Serializers?

Serializers permitem que dados complexos como QuerySets e instâncias de modelo sejam convertidos em tipos de dados nativos do Python que podem ser facilmente renderizados em JSON, XML ou outros formatos.

## Estrutura Básica

```python
from rest_framework import serializers

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'email', 'criado_em']
```

## Tipos de Serializers

1. **ModelSerializer**
```python
class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
```

2. **Serializer Regular**
```python
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
```

## Validação

```python
def validate_preco(self, value):
    if value < 0:
        raise serializers.ValidationError("Preço não pode ser negativo")
    return value

def validate(self, data):
    if data['preco'] > data['preco_maximo']:
        raise serializers.ValidationError("Preço excede o máximo")
    return data
```

## Relacionamentos

```python
class PedidoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    produtos = ProdutoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'produtos', 'total']
```
