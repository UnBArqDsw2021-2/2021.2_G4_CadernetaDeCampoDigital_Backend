from agrotoxico.models import Agrotoxico

from core.consts.agrotoxicos import ESTADOS_CHOICES

from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

from plantio.models.plantio import Plantio

import uuid


class AplicacaoAgrotoxico(models.Model):
    idAplicacao = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plantio = models.ForeignKey(Plantio, on_delete=models.PROTECT)
    agrotoxico = models.ForeignKey(Agrotoxico, null=True, on_delete=models.PROTECT)
    dataAplicacao = models.DateField()
    # TODO: Implementação de foto (Azure) -> issue 152
    # caminhoFotoAgrotoxico = models.CharField(max_length=255)
    dosagemAplicacao = models.DecimalField(
        max_digits=3, decimal_places=2, null=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    estadoAnalise = models.CharField(max_length=1, choices=ESTADOS_CHOICES, default='A')
