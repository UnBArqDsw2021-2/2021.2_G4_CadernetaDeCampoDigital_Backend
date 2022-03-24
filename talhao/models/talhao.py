from django.db import models

from propriedade.models import Propriedade

import uuid


class Talhao(models.Model):
    idTalhao = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idPropriedade = models.ForeignKey(Propriedade, on_delete=models.PROTECT)
    numero = models.PositiveIntegerField()

    class Meta:
        unique_together = ['idPropriedade', 'numero']
