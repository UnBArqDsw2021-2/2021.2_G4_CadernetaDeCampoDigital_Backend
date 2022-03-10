from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

import uuid


class Usuario(AbstractUser):
    PRODUTOR = 'produtor'
    TECNICO = 'tecnico'
    TIPO_ESCOLHAS = [
        (PRODUTOR, 'produtor'),
        (TECNICO, 'tecnico')
    ]

    idUsuario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpf = models.CharField(max_length=11, unique=True)
    dataNascimento = models.DateField()
    telefone = PhoneNumberField()
    nome = models.CharField(max_length=80)
    tipo = models.CharField(max_length=8, choices=TIPO_ESCOLHAS)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELD = []
