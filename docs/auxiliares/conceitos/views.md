# Django Views e ViewSets

## O que são Views?

Views são funções ou classes Python que processam requisições HTTP e retornam respostas. No DRF, ViewSets fornecem uma abstração para operações CRUD comuns.

## Tipos de Views

1. **ViewSets**
```python
from rest_framework import viewsets

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]
```

2. **APIView**
```python
from rest_framework.views import APIView

class PedidoView(APIView):
    def get(self, request):
        pedidos = Pedido.objects.all()
        return Response(PedidoSerializer(pedidos, many=True).data)
```

## Filtros e Paginação

```python
from rest_framework import filters

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'categoria']
    pagination_class = StandardResultsSetPagination
```
```python
from rest_framework.views import APIView
from rest_framework.response import Response

class ClienteView(APIView):
    # GET - Listar
    def get(self, request):
        clientes = Cliente.objects.all()
        return Response(ClienteSerializer(clientes, many=True).data)
    
    # POST - Criar
    def post(self, request):
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    # PATCH - Atualizar parcial
    def patch(self, request, pk):
        cliente = Cliente.objects.get(pk=pk)
        serializer = ClienteSerializer(cliente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    # DELETE - Remover
    def delete(self, request, pk):
        cliente = Cliente.objects.get(pk=pk)
        cliente.delete()
        return Response(status=204)
```

### 3. ViewSets (Mais comum em APIs REST)
```python
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    # Configurações adicionais
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cidade', 'status']
    search_fields = ['nome', 'email']
    
    # Endpoint customizado
    @action(detail=True, methods=['post'])
    def desativar(self, request, pk=None):
        cliente = self.get_object()
        cliente.ativo = False
        cliente.save()
        return Response({'status': 'cliente desativado'})

    # Override de método padrão
    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)
```

## Exemplos de Uso Prático

### 1. View com Filtros e Paginação
```python
from app.utils.paginators import CustomPagination

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        # Filtros dinâmicos
        queryset = Pedido.objects.all()
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
```

### 2. View com Agregações
```python
class RelatorioVendas(APIView):
    def get(self, request):
        # Equivalente a GROUP BY em SQL
        vendas = Pedido.objects.values('status').annotate(
            total=Sum('valor'),
            quantidade=Count('id')
        )
        return Response(vendas)
```

### 3. View com Múltiplos Serializers
```python
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ClienteListSerializer
        return ClienteDetailSerializer
```

## Autenticação e Permissões

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class PedidoProtegido(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Só usuários autenticados chegam aqui
        return Response({"message": "autorizado"})
```

## Tratamento de Erros

```python
from rest_framework.exceptions import NotFound

class ClienteDetalhe(APIView):
    def get(self, request, pk):
        try:
            cliente = Cliente.objects.get(pk=pk)
            return Response(ClienteSerializer(cliente).data)
        except Cliente.DoesNotExist:
            raise NotFound("Cliente não encontrado")
```

## Integração com SQL Server

### View com Raw Query
```python
from django.db import connection

class RelatorioComplexo(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    c.nome,
                    COUNT(p.id) as total_pedidos,
                    SUM(p.valor) as valor_total
                FROM clientes c
                LEFT JOIN pedidos p ON p.cliente_id = c.id
                GROUP BY c.nome
            """)
            columns = [col[0] for col in cursor.description]
            return Response([
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ])
```

## Boas Práticas

1. **Use ViewSets para operações CRUD padrão**
2. **Implemente APIViews para endpoints específicos**
3. **Mantenha a lógica de negócio nos models/services**
4. **Use serializers para validação de dados**
5. **Implemente paginação para grandes conjuntos**
6. **Documente endpoints com drf-yasg/swagger**

## Considerações de Performance

1. **Use select_related/prefetch_related para otimizar queries**
2. **Implemente caching quando apropriado**
3. **Pagine resultados grandes**
4. **Use bulk operations para operações em lote**

Consulte a documentação específica de cada app para exemplos práticos de implementação no projeto.
