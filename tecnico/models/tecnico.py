from django.db import models

from usuario.models import Usuario


class Tecnico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.PROTECT)
    crea = models.CharField(max_length=10, unique=True)
    formacao = models.CharField(max_length=80)
    email = models.EmailField(max_length=120)
    emailVerificado = models.BooleanField()
