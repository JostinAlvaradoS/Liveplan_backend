# Generated by Django 4.1.7 on 2024-09-17 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('livePlan', '0006_composicionfinanciamiento'),
    ]

    operations = [
        migrations.CreateModel(
            name='ventasMes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('anio1', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('anio2', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('anio3', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('anio4', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('anio5', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('planNegocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.plannegocio')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.producto_servicio')),
            ],
        ),
    ]