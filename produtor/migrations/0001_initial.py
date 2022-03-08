# Generated by Django 3.1.7 on 2022-03-08 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produtor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dap', models.CharField(max_length=11, unique=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='usuario.usuario')),
            ],
        ),
    ]
