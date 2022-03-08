from django.db import models

from usuario.models import Usuario


class Produtor(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)
    dap = models.CharField(max_length=11, unique=True)
