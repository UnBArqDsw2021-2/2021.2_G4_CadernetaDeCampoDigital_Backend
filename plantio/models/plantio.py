from core.consts.estados import UF_CHOICES

# from cultura.models import Cultura

from django.db import models
from django.core.validators import MinValueValidator

from talhao.models import Talhao

import uuid


class Plantio(models.Model):
    idPlantio = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # cultura = models.ForeignKey(Cultura, on_delete=models.PROTECT)
    talhao = models.ForeignKey(Talhao, on_delete=models.PROTECT)
    dataPlantio = models.DateField()
    estado = models.CharField(max_length=2, choices=UF_CHOICES)
