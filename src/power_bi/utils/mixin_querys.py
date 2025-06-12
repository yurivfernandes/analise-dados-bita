from django.db.models import QuerySet

from correios.models import TblCepNLogradouro

from ..models import (
    SolarInterfaceOriginal,
    SolarNodeOriginal,
    SolarNomeClienteCorreto,
    SolarNomeOperadoraCorreto,
    SolarNomeTecnologiaCorreto,
)


class MixinQuerys:
    """MÉTODOS COMUNS PARA USO NAS VIEWS."""
    
    def get_solar_node_original_queryset(self) -> QuerySet:
        """Retorna o queryset com o nome correto do cliente"""
        return SolarNodeOriginal.objects.using("power_bi").filter(
            **self._filtro
        )

    def get_solar_interface_original_queryset(self) -> QuerySet:
        """Retorna o queryset com os dados de [SolarInterfaceOriginal]"""
        return SolarInterfaceOriginal.objects.using("power_bi").filter(
            **self._filtro
        )

    def get_nome_operadora_correto_queryset(self) -> QuerySet:
        """Retorna o queryset com os dados de operadoras do model [SolarNomeOperadoraCorreto]"""
        return SolarNomeOperadoraCorreto.objects.using("power_bi")

    def get_nome_tecnologia_correto_queryset(self) -> QuerySet:
        """Retorna o queryset com os dados de tecnologia do model [SolarNomeTecnologiaCorreto]"""
        return SolarNomeTecnologiaCorreto.objects.using("power_bi")

    def get_nome_cliente_correto_queryset(self) -> QuerySet:
        """Retorna o queryset com os dados de cliente do model [SolarNomeClienteCorreto]"""
        return SolarNomeClienteCorreto.objects.using("power_bi")

    def get_uf_and_municipio_queryset(self) -> QuerySet:
        """Retorna o queryset com os dados de uf e município por cep do model [SolarNomeClienteCorreto]"""
        return TblCepNLogradouro.objects.using("correios")
