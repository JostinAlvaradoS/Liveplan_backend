from django.db import models

class planNegocio(models.Model):
    id = models.AutoField(primary_key=True)
    autor = models.CharField(max_length=90)
    problematica = models.TextField()

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