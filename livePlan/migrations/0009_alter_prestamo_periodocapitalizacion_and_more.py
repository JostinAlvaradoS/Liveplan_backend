# Generated by Django 4.1.7 on 2024-09-26 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livePlan', '0008_prestamo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='periodoCapitalizacion',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='prestamo',
            name='periodosAmortizacion',
            field=models.IntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='FinanciamientoInversiones',
        ),
    ]
