from django.db import models

class planNegocio(models.Model):
    id = models.AutoField(primary_key=True)
    autor = models.CharField(max_length=90)
    problematica = models.CharField(max_length=300)
    descripcion = models.TextField()
    

class inversionInicial(models.Model):
    id = models.AutoField(primary_key=True)
    planNegocio = models.ForeignKey(planNegocio, on_delete=models.CASCADE)
    seccion = models.CharField(max_length=100)
    importe = models.IntegerField(null=False)

class detalleInversionInicial(models.Model):
    id = models.AutoField(primary_key=True)
    seccion = models.ForeignKey(inversionInicial, on_delete=models.CASCADE)
    elemento = models.CharField(max_length=100)
    importe = models.IntegerField(null=False)
    vida_util = models.IntegerField(null=True)

class Supuesto(models.Model):
    id = models.AutoField(primary_key=True)
    planNegocio = models.ForeignKey(planNegocio, on_delete=models.CASCADE)
    porcentaje_ventas_inventario = models.IntegerField()
    variacion_porcentaje_ventas_credito = models.IntegerField()
    ptu_se_paga_al_siguiente_ano = models.IntegerField()
    isr_se_paga_al_siguiente_mes = models.IntegerField()


class Producto_servicio(models.Model):
    id = models.AutoField(primary_key=True)
    planNegocio = models.ForeignKey(planNegocio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200, blank=False)

class VentaDiaria(models.Model):
    id = models.AutoField(primary_key=True)
    planNegocio = models.ForeignKey(planNegocio, on_delete=models.CASCADE)
    producto_servicio = models.ForeignKey(Producto_servicio,on_delete=models.CASCADE)
    ventas_por_dia = models.IntegerField()

class VariacionAnual(models.Model):
    id = models.AutoField(primary_key=True)
    planNegocio = models.ForeignKey(planNegocio, on_delete=models.CASCADE)
    anio = models.IntegerField()
    porcentaje = models.IntegerField()


class PrecioVenta(models.Model):
    id = models.AutoField(primary_key=True)
    planNegocio = models.ForeignKey(planNegocio, on_delete=models.CASCADE)
    producto_servicio = models.ForeignKey(Producto_servicio,on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)


class Categorias_costos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)


class Costo(models.Model):
    id = models.AutoField(primary_key=True)
    planNegocio = models.ForeignKey(planNegocio, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categorias_costos, on_delete=models.CASCADE)
    producto_servicio = models.ForeignKey(Producto_servicio,on_delete=models.CASCADE)
    costo = models.DecimalField(max_digits=10, decimal_places=3)

class IndicadoresMacro(models.Model):
    id = models.AutoField(primary_key=True)
    planNegocio = models.ForeignKey(planNegocio, on_delete=models.CASCADE)
    tipoCambio = models.DecimalField(max_digits=10,decimal_places=3)
    inflacionAnual = models.DecimalField(max_digits=10,decimal_places=3)
    tasaInteresDeuda = models.DecimalField(max_digits=10,decimal_places=3)
    tasaInteresInversiones = models.DecimalField(max_digits=10,decimal_places=3)
    tasaImpuesto = models.IntegerField()
    ptu = models.IntegerField()
    diasporMes = models.IntegerField()

class ComposicionFinanciamiento(models.Model):
    id = models.AutoField(primary_key=True)
    planNegocio = models.ForeignKey(planNegocio, on_delete=models.CASCADE)
    capitalSocial = models.IntegerField()
    deuda = models.IntegerField()

class FinanciamientoInversiones(models.Model):
    id = models.AutoField(primary_key=True)
    planNegocio = models.ForeignKey(planNegocio, on_delete=models.CASCADE)
    capitalSocial = models.IntegerField()
    deuda = models.IntegerField()

class proyeccionVentas(models.Model):
    id = models.AutoField(primary_key=True)
    planNegocio = models.ForeignKey(planNegocio, on_delete=models.CASCADE)
    producto_servicio = models.ForeignKey(Producto_servicio, on_delete=models.CASCADE)
    anio = models.IntegerField()
    ventas_mensuales = models.JSONField()  


class depreciacionMensual(models.Model):
    id = models.AutoField(primary_key=True)
    planNegocio = models.ForeignKey(planNegocio, on_delete=models.CASCADE)
    inversion = models.ForeignKey(detalleInversionInicial, on_delete=models.CASCADE)
    depreciacionMensual = models.DecimalField(max_digits=10,decimal_places=3, null=True)
    depreciacion_anio1 = models.IntegerField( null=True)
    depreciacion_anio2 = models.IntegerField( null=True)
    depreciacion_anio3 = models.IntegerField( null=True)
    depreciacion_anio4 = models.IntegerField( null=True)
    depreciacion_anio5 = models.IntegerField( null=True)
    valor_rescate = models.IntegerField(null=True) 


class ventasMes(models.Model):
    id = models.AutoField(primary_key=True)
    planNegocio = models.ForeignKey(planNegocio, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto_servicio, on_delete=models.CASCADE)
    anio1 = models.DecimalField(max_digits=10,decimal_places=3, null=True)
    anio2 = models.DecimalField(max_digits=10,decimal_places=3, null=True)
    anio3 = models.DecimalField(max_digits=10,decimal_places=3, null=True)
    anio4 = models.DecimalField(max_digits=10,decimal_places=3, null=True)
    anio5 = models.DecimalField(max_digits=10,decimal_places=3, null=True)

class gastosOperacion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField()
    referencia = models.DecimalField(max_digits=10,decimal_places=3, null=True)
    