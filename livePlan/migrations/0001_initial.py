# Generated by Django 4.1.7 on 2024-09-01 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias_costos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='planNegocio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('autor', models.CharField(max_length=90)),
                ('problematica', models.CharField(max_length=300)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Producto_servicio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('planNegocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.plannegocio')),
            ],
        ),
        migrations.CreateModel(
            name='VentaDiaria',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ventas_por_dia', models.IntegerField()),
                ('planNegocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.plannegocio')),
                ('producto_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.producto_servicio')),
            ],
        ),
        migrations.CreateModel(
            name='VariacionAnual',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('anio', models.IntegerField()),
                ('porcentaje', models.IntegerField()),
                ('planNegocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.plannegocio')),
            ],
        ),
        migrations.CreateModel(
            name='Supuesto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('porcentaje_ventas_inventario', models.IntegerField()),
                ('variacion_porcentaje_ventas_credito', models.IntegerField()),
                ('ptu_se_paga_al_siguiente_ano', models.IntegerField()),
                ('isr_se_paga_al_siguiente_mes', models.IntegerField()),
                ('planNegocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.plannegocio')),
            ],
        ),
        migrations.CreateModel(
            name='PrecioVenta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('planNegocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.plannegocio')),
                ('producto_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.producto_servicio')),
            ],
        ),
        migrations.CreateModel(
            name='inversionInicial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('seccion', models.CharField(max_length=100)),
                ('importe', models.IntegerField()),
                ('planNegocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.plannegocio')),
            ],
        ),
        migrations.CreateModel(
            name='detalleInversionInicial',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('elemento', models.CharField(max_length=100)),
                ('importe', models.IntegerField()),
                ('seccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.inversioninicial')),
            ],
        ),
        migrations.CreateModel(
            name='Costo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('costo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.categorias_costos')),
                ('planNegocio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.plannegocio')),
                ('producto_servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livePlan.producto_servicio')),
            ],
        ),
    ]
