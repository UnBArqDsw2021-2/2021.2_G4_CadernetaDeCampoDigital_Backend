from django.db import models
from django.utils.translation import gettext_lazy as _


class AplicacaoEstados(models.TextChoices):
    SUCESSO = 'S', _('Sucesso')
    PROBLEMA = 'P', _('Com Problema(s)')
    ANALISE = 'A', _('Em Análise')
