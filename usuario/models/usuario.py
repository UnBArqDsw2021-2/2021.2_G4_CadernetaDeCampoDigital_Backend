from core.consts.usuarios import TIPO_CHOICES

from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

import uuid


class Usuario(AbstractUser):
    idUsuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpf = models.CharField(max_length=11, unique=True)
    dataNascimento = models.DateField()
    telefone = PhoneNumberField()
    nome = models.CharField(max_length=80)
    tipo = models.CharField(max_length=8, choices=TIPO_CHOICES)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELD = []
