# Serializers

## O que são serializers?

Serializers no app **power_bi** são responsáveis por converter modelos Django em JSON para APIs REST e vice-versa, além de permitir validação e customização dos dados expostos.

---

## Para que servem?

- **Serializar**: Transformar objetos do banco de dados em JSON para resposta de API.
- **Desserializar**: Validar e transformar dados recebidos (JSON) em objetos Python/modelos.
- **Validação**: Garantir que os dados recebidos estão corretos antes de salvar no banco.

---

## Exemplo básico de utilização

```python
from rest_framework import serializers
from ...models import TblSolarInterfacesVgr

class SolarInterfacesVgrSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblSolarInterfacesVgr
        fields = "__all__"
```

- O serializer acima converte todos os campos do modelo `TblSolarInterfacesVgr` para JSON e valida dados recebidos para criação/atualização.

---

## Exemplos avançados

- Você pode criar serializers que retornam apenas campos específicos, campos calculados ou fazem validação customizada, assim como mostrado na documentação do DW Analytics.

---

## Como usar

- Crie um serializer para cada modelo que será exposto via API.
- Use o serializer nas views para transformar dados de entrada e saída.
- Pode customizar métodos de validação ou campos conforme necessário.

---

Consulte os arquivos individuais para detalhes de cada serializer.
