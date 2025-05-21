# Django Tests

## O que são Tests?

Testes são fundamentais para garantir que seu código funcione como esperado e continue funcionando após mudanças.

## Tipos de Testes

1. **Unit Tests**
```python
from django.test import TestCase

class ProdutoTestCase(TestCase):
    def setUp(self):
        self.produto = Produto.objects.create(
            nome="Test",
            preco=10.00
        )

    def test_produto_criacao(self):
        self.assertEqual(self.produto.nome, "Test")
```

2. **API Tests**
```python
from rest_framework.test import APITestCase

class ProdutoAPITestCase(APITestCase):
    def test_lista_produtos(self):
        response = self.client.get('/api/produtos/')
        self.assertEqual(response.status_code, 200)
```
