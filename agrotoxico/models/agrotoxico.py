from django.db import models

import uuid

from cultura.models.cultura import Cultura

from .tipo_agrotoxico import TipoAgrotoxico


class Agrotoxico(models.Model):
    idAgrotoxico = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=80, unique=True)
    tipo = models.ForeignKey(TipoAgrotoxico, on_delete=models.PROTECT)

    @property
    def espera(self):
        return self.esperas_set


class Espera(models.Model):
    cultura = models.ForeignKey(Cultura, on_delete=models.PROTECT)
    agrotoxico = models.ForeignKey(Agrotoxico, on_delete=models.PROTECT)
    diasCarencia = models.PositiveIntegerField()

    class Meta:
        unique_together = [('cultura', 'agrotoxico')]
