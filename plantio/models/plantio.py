from core.consts.plantios import PLANTIO_CHOICES

from cultura.models import Cultura

from django.db import models

from talhao.models import Talhao

import uuid


class Plantio(models.Model):
    idPlantio = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cultura = models.ForeignKey(Cultura, on_delete=models.PROTECT)
    talhao = models.ForeignKey(Talhao, on_delete=models.PROTECT)
    dataPlantio = models.DateField()
    estado = models.CharField(max_length=10, choices=PLANTIO_CHOICES)
