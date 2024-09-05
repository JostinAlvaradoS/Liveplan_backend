


def calcular_ventas_mensuales(ventas_por_dia, porcentaje):
    return [ventas_por_dia * (1 + (porcentaje / 100)) for _ in range(12)]