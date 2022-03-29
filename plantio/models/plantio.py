from agrotoxico.models import Agrotoxico

from core.consts.plantios import PLANTIO_CHOICES
from core.consts.agrotoxicos import ESTADOS_CHOICES

from cultura.models import Cultura

from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

from talhao.models import Talhao

import uuid


class Plantio(models.Model):
    idPlantio = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cultura = models.ForeignKey(Cultura, on_delete=models.PROTECT)
    talhao = models.ForeignKey(Talhao, on_delete=models.PROTECT)
    dataPlantio = models.DateField()
    estado = models.CharField(max_length=10, choices=PLANTIO_CHOICES)
    agrotoxico = models.ManyToManyField(Agrotoxico, through='AssociacaoPlantioAgrotoxico')


class AssociacaoPlantioAgrotoxico(models.Model):
    plantio = models.ForeignKey(Plantio, on_delete=models.PROTECT)
    agrotoxico = models.ForeignKey(Agrotoxico, on_delete=models.PROTECT)
    dataAplicacao = models.DateField()
    # TODO: Implementação de foto (Azure) -> issue 152
    # caminhoFotoAgrotoxico = models.CharField(max_length=255)
    dosagemAplicacao = models.DecimalField(
        max_digits=3, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    estadoAnalise = models.CharField(max_length=1, choices=ESTADOS_CHOICES, default='A')

    class Meta:
        unique_together = [('plantio', 'agrotoxico', 'dataAplicacao')]
