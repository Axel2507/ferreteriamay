# Generated by Django 5.2 on 2025-04-27 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria',
            name='descripcion',
        ),
        migrations.AddField(
            model_name='categoria',
            name='abreviacion',
            field=models.CharField(default='HMM', max_length=3, unique=True),
        ),
    ]
