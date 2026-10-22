"""Funciones de cálculo. Este archivo no usa Streamlit ni imprime resultados."""

IVA_PORCENTAJE = 0.21
DESCUENTO_EFECTIVO = 0.10

def buscar_posicion(lista_productos, producto):
    """Devuelve el índice del producto o -1 si no está."""
    try:
        return lista_productos.index(producto)
    except ValueError:
        return -1

def calcular_subtotal(cantidades, precios_unitarios):
    """Suma cantidad por precio unitario para todos los renglones."""
    subtotal = sum(cantidad * precio for cantidad, precio in zip(cantidades, precios_unitarios))
    return round(subtotal, 2)

def calcular_descuento(subtotal, forma_pago, efectivo):
    """Aplica 10% de descuento solo cuando el pago es en efectivo."""
    descuento = subtotal * DESCUENTO_EFECTIVO if forma_pago == efectivo else 0
    return round(descuento, 2)

def calcular_iva(subtotal, descuento):
    """Calcula 21% sobre el subtotal después del descuento."""
    return round((subtotal - descuento) * IVA_PORCENTAJE, 2)

def calcular_total(subtotal, descuento, iva):
    """Devuelve el total final."""
    return round(subtotal - descuento + iva, 2)

def calcular_presupuesto(cantidades, precios_unitarios, forma_pago, efectivo):
    """Devuelve subtotal, descuento, IVA y total."""
    subtotal = calcular_subtotal(cantidades, precios_unitarios)
    descuento = calcular_descuento(subtotal, forma_pago, efectivo)
    iva = calcular_iva(subtotal, descuento)
    total = calcular_total(subtotal, descuento, iva)
    return subtotal, descuento, iva, total
