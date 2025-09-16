from django.core.management.base import BaseCommand

from ...models import AvaliacaoTecnica


class Command(BaseCommand):
    help = "Popula a tabela AvaliacaoTecnica com todos os dados de classificação técnica"

    def handle(self, *args, **kwargs):
        notas_por_criterio = {
            "JITTER": {"OTIMO": 20, "BOM": 16, "RUIM": 10},
            "LATENCIA": {"OTIMO": 30, "BOM": 24, "RUIM": 15},
            "PERDA_PACOTE": {"OTIMO": 50, "BOM": 40, "RUIM": 25},
        }

        dados = [
            (
                "FIXA",
                "CAPITAL",
                "JITTER",
                [(0, 30, "OTIMO"), (31, 60, "BOM"), (61, None, "RUIM")],
            ),
            (
                "FIXA",
                "CAPITAL",
                "LATENCIA",
                [(0, 100, "OTIMO"), (101, 150, "BOM"), (151, None, "RUIM")],
            ),
            (
                "FIXA",
                "CAPITAL",
                "PERDA_PACOTE",
                [(0, 2.0, "OTIMO"), (2.1, 8.0, "BOM"), (8.1, None, "RUIM")],
            ),
            (
                "FIXA",
                "INTERIOR",
                "JITTER",
                [(0, 36, "OTIMO"), (37, 72, "BOM"), (73, None, "RUIM")],
            ),
            (
                "FIXA",
                "INTERIOR",
                "LATENCIA",
                [(0, 120, "OTIMO"), (121, 180, "BOM"), (181, None, "RUIM")],
            ),
            (
                "FIXA",
                "INTERIOR",
                "PERDA_PACOTE",
                [(0, 2.4, "OTIMO"), (2.5, 9.6, "BOM"), (9.7, None, "RUIM")],
            ),
            (
                "MOVEL",
                "CAPITAL",
                "JITTER",
                [(0, 20, "OTIMO"), (21, 80, "BOM"), (81, None, "RUIM")],
            ),
            (
                "MOVEL",
                "CAPITAL",
                "LATENCIA",
                [(0, 100, "OTIMO"), (101, 200, "BOM"), (201, None, "RUIM")],
            ),
            (
                "MOVEL",
                "CAPITAL",
                "PERDA_PACOTE",
                [(0, 5.0, "OTIMO"), (5.1, 10.0, "BOM"), (10.1, None, "RUIM")],
            ),
            (
                "MOVEL",
                "INTERIOR",
                "JITTER",
                [(0, 24, "OTIMO"), (25, 96, "BOM"), (97, None, "RUIM")],
            ),
            (
                "MOVEL",
                "INTERIOR",
                "LATENCIA",
                [(0, 120, "OTIMO"), (121, 240, "BOM"), (241, None, "RUIM")],
            ),
            (
                "MOVEL",
                "INTERIOR",
                "PERDA_PACOTE",
                [(0, 6.0, "OTIMO"), (6.1, 12.0, "BOM"), (12.1, None, "RUIM")],
            ),
            (
                "SATELITE",
                "CAPITAL",
                "JITTER",
                [(0, 60, "OTIMO"), (61, 120, "BOM"), (121, None, "RUIM")],
            ),
            (
                "SATELITE",
                "CAPITAL",
                "LATENCIA",
                [(0, 200, "OTIMO"), (201, 600, "BOM"), (601, None, "RUIM")],
            ),
            (
                "SATELITE",
                "CAPITAL",
                "PERDA_PACOTE",
                [(0, 3.0, "OTIMO"), (3.1, 10.0, "BOM"), (10.1, None, "RUIM")],
            ),
            (
                "IP_DEDICADO",
                "CAPITAL",
                "JITTER",
                [(0, 10, "OTIMO"), (11, 40, "BOM"), (41, None, "RUIM")],
            ),
            (
                "IP_DEDICADO",
                "CAPITAL",
                "LATENCIA",
                [(0, 50, "OTIMO"), (51, 100, "BOM"), (101, None, "RUIM")],
            ),
            (
                "IP_DEDICADO",
                "CAPITAL",
                "PERDA_PACOTE",
                [(0, 1.0, "OTIMO"), (1.1, 5.0, "BOM"), (5.1, None, "RUIM")],
            ),
            (
                "IP_DEDICADO",
                "INTERIOR",
                "JITTER",
                [(0, 12, "OTIMO"), (13, 48, "BOM"), (49, None, "RUIM")],
            ),
            (
                "IP_DEDICADO",
                "INTERIOR",
                "LATENCIA",
                [(0, 60, "OTIMO"), (61, 120, "BOM"), (121, None, "RUIM")],
            ),
            (
                "IP_DEDICADO",
                "INTERIOR",
                "PERDA_PACOTE",
                [(0, 1.2, "OTIMO"), (1.3, 6.0, "BOM"), (6.1, None, "RUIM")],
            ),
            (
                "MPLS",
                "CAPITAL",
                "JITTER",
                [(0, 10, "OTIMO"), (11, 40, "BOM"), (41, None, "RUIM")],
            ),
            (
                "MPLS",
                "CAPITAL",
                "LATENCIA",
                [(0, 50, "OTIMO"), (51, 100, "BOM"), (101, None, "RUIM")],
            ),
            (
                "MPLS",
                "CAPITAL",
                "PERDA_PACOTE",
                [(0, 1.0, "OTIMO"), (1.1, 5.0, "BOM"), (5.1, None, "RUIM")],
            ),
            (
                "MPLS",
                "INTERIOR",
                "JITTER",
                [(0, 12, "OTIMO"), (13, 48, "BOM"), (49, None, "RUIM")],
            ),
            (
                "MPLS",
                "INTERIOR",
                "LATENCIA",
                [(0, 60, "OTIMO"), (61, 120, "BOM"), (121, None, "RUIM")],
            ),
            (
                "MPLS",
                "INTERIOR",
                "PERDA_PACOTE",
                [(0, 1.2, "OTIMO"), (1.3, 6.0, "BOM"), (6.1, None, "RUIM")],
            ),
        ]

        for tecnologia, regiao, criterio, faixas in dados:
            for faixa_min, faixa_max, classificacao in faixas:
                nota = notas_por_criterio[criterio][classificacao]
                self.criar(
                    tecnologia=getattr(
                        AvaliacaoTecnica.Tecnologia, tecnologia
                    ),
                    regiao=getattr(AvaliacaoTecnica.Regiao, regiao),
                    criterio=getattr(AvaliacaoTecnica.Criterio, criterio),
                    faixa_min=faixa_min,
                    faixa_max=faixa_max,
                    classificacao=getattr(
                        AvaliacaoTecnica.Classificacao, classificacao
                    ),
                    nota=nota,
                )

        self.stdout.write(
            self.style.SUCCESS("✅ Avaliações técnicas populadas com sucesso!")
        )

    def criar(
        self,
        tecnologia,
        regiao,
        criterio,
        faixa_min,
        faixa_max,
        classificacao,
        nota,
    ):
        AvaliacaoTecnica.objects.create(
            tecnologia=tecnologia,
            regiao=regiao,
            criterio=criterio,
            faixa_min=faixa_min,
            faixa_max=faixa_max,
            classificacao=classificacao,
            nota=nota,
        )
