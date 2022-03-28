from django.db import models

import uuid


class Cultura(models.Model):
    idCultura = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=80, unique=True)
