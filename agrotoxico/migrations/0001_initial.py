# Generated by Django 3.1.7 on 2022-03-27 23:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoAgrotoxico',
            fields=[
                ('idTipoAgrotoxico', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=80, unique=True)),
            ],
        ),
    ]
