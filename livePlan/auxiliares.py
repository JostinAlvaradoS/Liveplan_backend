


from decimal import Decimal
from livePlan.models import ComposicionFinanciamiento, IndicadoresMacro, inversionInicial, planNegocio, prestamo

from django.db.models import Sum
def calcular_ventas_mensuales(ventas_por_dia, porcentaje):
    return [ventas_por_dia * (1 + (porcentaje / 100)) for _ in range(12)]

def calcular_intereses(plan_negocio):
    try:
        # Verificar existencia del plan de negocio
        try:
            plan_negocio_obj = planNegocio.objects.get(id=plan_negocio)
        except planNegocio.DoesNotExist:
            return {"error": "El plan de negocio no existe."}

        # Verificar si existe un préstamo asociado
        prestamo_existente = prestamo.objects.filter(planNegocio=plan_negocio_obj).first()
        if not prestamo_existente:
            return {"error": "No existe un préstamo asociado al plan de negocio."}

        # Verificar que todos los datos necesarios están presentes
        if (prestamo_existente.periodoCapitalizacion is None or
            prestamo_existente.tasaInteresMensual is None or
            prestamo_existente.periodosAmortizacion is None):
            return {"error": "Datos faltantes para realizar el cálculo de intereses."}

        # Obtener el monto total de inversión y deuda
        inversiones = inversionInicial.objects.filter(planNegocio=plan_negocio_obj).aggregate(total_importes=Sum('importe'))['total_importes']
        deuda_porcentaje = ComposicionFinanciamiento.objects.get(planNegocio=plan_negocio_obj).deuda / Decimal(100)
        tasa_anual = IndicadoresMacro.objects.filter(planNegocio_id=plan_negocio).first()
        tasa_anual = tasa_anual.tasaInteresDeuda / Decimal(100)
        monto_total_deuda = Decimal(inversiones) * deuda_porcentaje

        tasa_interes_mensual = Decimal(prestamo_existente.tasaInteresMensual) / Decimal(100)

        # Calcular intereses mensuales y totales anuales
        reporte = {}
        saldo_inicial = monto_total_deuda

        for mes in range(1, 61):
            intereses = saldo_inicial * tasa_interes_mensual
            saldo_inicial -= (prestamo_existente.cuotaFijaMensual - intereses)

            # Asignar cada mes a la clave correspondiente
            reporte[f"interesesMes{mes}"] = float(intereses)

            # Agregar totales anuales al final de cada año
            if mes % 12 == 0:
                anio = mes // 12
                total_anual = sum(reporte[f"interesesMes{m}"] for m in range((anio - 1) * 12 + 1, anio * 12 + 1))
                reporte[f"interesesAnio{anio}"] = float(total_anual)

        return reporte

    except Exception as e:
        return {"error": str(e)}



