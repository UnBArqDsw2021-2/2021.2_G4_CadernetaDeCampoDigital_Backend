# Generated by Django 3.1.14 on 2022-04-07 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantio', '0002_aplicacaoagrotoxico'),
    ]

    operations = [
        migrations.AddField(
            model_name='aplicacaoagrotoxico',
            name='fotoAgrotoxico',
            field=models.ImageField(max_length=255, null=True, upload_to=''),
        ),
    ]
