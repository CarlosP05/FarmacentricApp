# Importamos nuestro catálogo desde la carpeta de datos
# logica_pos.py (Actualizado)

from Datos.datos_inventario import catalogo_productos, lotes_inventario
# Importamos datetime para manejar las fechas de caducidad
from datetime import datetime

def buscar_producto_por_id(id_producto):
    for producto in catalogo_productos:
        if producto["id_producto"] == id_producto:
            return producto
    return None
def calcular_venta(carrito):
    """
    Recibe una lista de artículos (el carrito de compras) y calcula los totales
    sin descontar del inventario (solo para previsualizar el ticket).
    """
    total_cordobas = 0.0
    detalle_factura = []
    alertas_receta = []

    for item in carrito:
        producto = buscar_producto_por_id(item["id_producto"])
        
        if producto:
            subtotal = producto["precio_venta"] * item["cantidad"]
            total_cordobas += subtotal
            
            # Guardamos el detalle limpio para el ticket
            detalle_factura.append({
                "producto": producto["nombre"],
                "cantidad": item["cantidad"],
                "precio_uni": producto["precio_venta"],
                "subtotal": subtotal
            })
            
            # Verificamos si requiere receta
            if producto["requiere_receta"]:
                alertas_receta.append(producto["nombre"])

    # Retornamos todo empacado en un diccionario
    return {
        "exito": True,
        "detalle": detalle_factura,
        "total_pagar": total_cordobas,
        "pedir_recetas_para": alertas_receta
    }

def calcular_stock_total(id_producto):
    """Calcula el stock real sumando todos los lotes vigentes de un producto."""
    total = 0
    for lote in lotes_inventario:
        if lote["id_producto"] == id_producto:
            total += lote["cantidad_actual"]
    return total

def descontar_stock_fefo(id_producto, cantidad_a_vender):
    """
    Descuenta el stock utilizando el método FEFO (First Expired, First Out).
    Devuelve True si había suficiente stock, False si no.
    """
    # 1. Obtenemos todos los lotes de este producto que tengan stock > 0
    lotes_del_producto = [
        lote for lote in lotes_inventario 
        if lote["id_producto"] == id_producto and lote["cantidad_actual"] > 0
    ]
    
    # 2. Verificamos si hay stock suficiente en total
    stock_total_disponible = sum(lote["cantidad_actual"] for lote in lotes_del_producto)
    if cantidad_a_vender > stock_total_disponible:
        return False # Quiebre de stock, no se puede realizar la venta
        
    # 3. Ordenamos los lotes por fecha de vencimiento (el más próximo primero)
    # datetime.strptime convierte el texto "2026-09-15" en una fecha real para poder ordenarla
    lotes_del_producto.sort(key=lambda x: datetime.strptime(x["fecha_vencimiento"], "%Y-%m-%d"))
    
    # 4. Consumo lógico iterativo (La magia del sistema)
    cantidad_restante = cantidad_a_vender
    
    for lote in lotes_del_producto:
        if cantidad_restante == 0:
            break # Ya descontamos todo lo necesario
            
        if lote["cantidad_actual"] >= cantidad_restante:
            # Si este lote tiene suficiente para cubrir lo que falta
            lote["cantidad_actual"] -= cantidad_restante
            cantidad_restante = 0
        else:
            # Si este lote no alcanza, lo vaciamos y seguimos con el próximo
            cantidad_restante -= lote["cantidad_actual"]
            lote["cantidad_actual"] = 0
            
    return True

def procesar_venta(carrito):
    """
    Procesa la venta y ejecuta el descuento del inventario.
    """
    total_cordobas = 0.0
    
    # Paso 1: Validar que haya stock suficiente para TODO el carrito antes de cobrar
    for item in carrito:
        stock_actual = calcular_stock_total(item["id_producto"])
        if item["cantidad"] > stock_actual:
            producto = buscar_producto_por_id(item["id_producto"])
            return {
                "exito": False,
                "mensaje": f"Error: Stock insuficiente para '{producto['nombre']}'. Solicitado: {item['cantidad']}, Disponible: {stock_actual}."
            }
            
    # Paso 2: Si hay stock de todo, procedemos a cobrar y descontar
    for item in carrito:
        producto = buscar_producto_por_id(item["id_producto"])
        
        # Calcular dinero
        total_cordobas += (producto["precio_venta"] * item["cantidad"])
        
        # Descontar del inventario físico (usando FEFO)
        descontar_stock_fefo(item["id_producto"], item["cantidad"])
        
    return {
        "exito": True,
        "mensaje": "Venta procesada con éxito. Inventario actualizado.",
        "total_cobrado": total_cordobas
    }

# ==========================================
# PRUEBAS EN CONSOLA
# ==========================================
if __name__ == "__main__":
    print("--- Estado Inicial del Paracetamol (ID 1001) ---")
    print(f"Stock total: {calcular_stock_total(1001)}")
    # Mostramos los lotes para ver cómo cambian
    for lote in lotes_inventario:
        if lote["id_producto"] == 1001:
            print(f"Lote: {lote['id_lote']} | Cantidad: {lote['cantidad_actual']} | Vence: {lote['fecha_vencimiento']}")

    print("\n--- Ejecutando venta de 15 cajas de Paracetamol ---")
    carrito_simulado = [{"id_producto": 1001, "cantidad": 15}]
    resultado = procesar_venta(carrito_simulado)
    print(resultado["mensaje"])

    print("\n--- Estado Final del Paracetamol (ID 1001) ---")
    print(f"Stock total: {calcular_stock_total(1001)}")
    for lote in lotes_inventario:
        if lote["id_producto"] == 1001:
            print(f"Lote: {lote['id_lote']} | Cantidad: {lote['cantidad_actual']} | Vence: {lote['fecha_vencimiento']}")