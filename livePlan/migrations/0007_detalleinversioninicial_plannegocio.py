# Generated by Django 5.1.2 on 2024-11-13 02:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livePlan', '0006_detalleinversioninicial_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalleinversioninicial',
            name='planNegocio',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='livePlan.plannegocio'),
            preserve_default=False,
        ),
    ]
