from django.db import models

from cultura.models import Cultura
from agrotoxico.models import Agrotoxico

class Espera(models.Model):
    cultura = models.ForeignKey(Cultura, on_delete=models.PROTECT)
    agrotoxico = models.ForeignKey(Agrotoxico, on_delete=models.PROTECT)
    diasCarencia = models.PositiveIntegerField()

    class Meta:
        unique_together = [('cultura', 'agrotoxico')]
