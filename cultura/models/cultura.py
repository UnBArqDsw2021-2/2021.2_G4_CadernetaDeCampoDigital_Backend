from django.db import models

import uuid

from agrotoxico.models import Agrotoxico


class Cultura(models.Model):
    idCultura = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=80, unique=True)
    agrotoxicos = models.ManyToManyField(Agrotoxico, through="espera")


class Espera(models.Model):
    cultura = models.ForeignKey(Cultura, on_delete=models.PROTECT)
    agrotoxico = models.ForeignKey(Agrotoxico, on_delete=models.PROTECT)
    diasCarencia = models.PositiveIntegerField()

    class Meta:
        unique_together = [('cultura', 'agrotoxico')]
