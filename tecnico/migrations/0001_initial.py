# Generated by Django 3.1.7 on 2022-03-10 00:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tecnico',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crea', models.CharField(max_length=10, unique=True)),
                ('formacao', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=120)),
                ('emailVerificado', models.BooleanField()),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='usuario.usuario')),
            ],
        ),
    ]