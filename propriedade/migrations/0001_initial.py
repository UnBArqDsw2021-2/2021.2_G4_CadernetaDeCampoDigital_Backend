# Generated by Django 3.1.7 on 2022-03-20 01:35

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tecnico', '0001_initial'),
        ('produtor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Propriedade',
            fields=[
                ('idPropriedade', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cep', models.CharField(max_length=8)),
                ('estado', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2)),
                ('cidade', models.CharField(max_length=40)),
                ('bairro', models.CharField(max_length=40)),
                ('logradouro', models.CharField(max_length=80)),
                ('complemento', models.CharField(max_length=80, null=True)),
                ('numeroCasa', models.PositiveIntegerField()),
                ('hectares', models.DecimalField(decimal_places=2, max_digits=6, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('produtor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='produtor.produtor')),
                ('tecnico', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tecnico.tecnico')),
            ],
        ),
    ]
