from core.consts.estados import UF_CHOICES

from django.db import models
from django.core.validators import MinValueValidator

from decimal import Decimal

import uuid

from produtor.models import Produtor
from tecnico.models import Tecnico


class Propriedade(models.Model):
    idPropriedade = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cep = models.CharField(max_length=8)
    estado = models.CharField(max_length=2, choices=UF_CHOICES)
    cidade = models.CharField(max_length=40)
    bairro = models.CharField(max_length=40)
    logradouro = models.CharField(max_length=80)
    complemento = models.CharField(max_length=80, null=True)
    numeroCasa = models.PositiveIntegerField()
    hectares = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    produtor = models.ForeignKey(Produtor, on_delete=models.PROTECT)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.SET_NULL, null=True, blank=True)
