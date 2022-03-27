from django.db import models

import uuid

from .tipo_agrotoxico import TipoAgrotoxico

class Agrotoxico(models.Model):
    idAgrotoxico = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=80, unique=True)
    tipo = models.ForeignKey(TipoAgrotoxico, on_delete=models.PROTECT)
