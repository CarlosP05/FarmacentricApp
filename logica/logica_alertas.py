from Datos.datos_inventario import catalogo_productos, lotes_inventario
from logica.logica_pos import calcular_stock_total # Reutilizamos la función que suma los lotes
from datetime import datetime, timedelta

def verificar_stock_bajo():
    """
    Compara el stock total de cada producto contra su stock mínimo.
    Retorna una lista con las alertas.
    """
    alertas_stock = []
    
    for producto in catalogo_productos:
        stock_actual = calcular_stock_total(producto["id_producto"])
        
        if stock_actual <= producto["stock_minimo"]:
            alertas_stock.append({
                "producto": producto["nombre"],
                "stock_actual": stock_actual,
                "stock_minimo": producto["stock_minimo"],
                "estado": "CRÍTICO" if stock_actual == 0 else "ADVERTENCIA"
            })
            
    return alertas_stock

def verificar_vencimientos_proximos(dias_alerta=90):
    """
    Revisa si algún lote vence en un plazo menor a 'dias_alerta' (por defecto 90 días).
    También avisa si un lote ya está vencido.
    """
    alertas_vencimiento = []
    hoy = datetime.now()
    
    # Calculamos la fecha límite (hoy + 90 días)
    fecha_limite = hoy + timedelta(days=dias_alerta)
    
    for lote in lotes_inventario:
        # Si el lote ya está vacío, lo ignoramos, no es un problema
        if lote["cantidad_actual"] == 0:
            continue
            
        # Convertimos la fecha de texto a un objeto fecha real
        fecha_vencimiento_lote = datetime.strptime(lote["fecha_vencimiento"], "%Y-%m-%d")
        
        # Buscamos el nombre del producto para que el reporte sea legible
        nombre_producto = "Desconocido"
        for prod in catalogo_productos:
            if prod["id_producto"] == lote["id_producto"]:
                nombre_producto = prod["nombre"]
                break
                
        # Evaluamos las fechas
        if fecha_vencimiento_lote < hoy:
            # ¡Ya venció! Pérdida financiera.
            alertas_vencimiento.append({
                "producto": nombre_producto,
                "lote": lote["id_lote"],
                "cantidad": lote["cantidad_actual"],
                "fecha": lote["fecha_vencimiento"],
                "estado": "VENCIDO - RETIRAR"
            })
        elif hoy <= fecha_vencimiento_lote <= fecha_limite:
            # Está próximo a vencer
            dias_restantes = (fecha_vencimiento_lote - hoy).days
            alertas_vencimiento.append({
                "producto": nombre_producto,
                "lote": lote["id_lote"],
                "cantidad": lote["cantidad_actual"],
                "fecha": lote["fecha_vencimiento"],
                "estado": f"VENCE EN {dias_restantes} DÍAS"
            })
            
    return alertas_vencimiento

def obtener_dashboard_alertas():
    """
    Empaqueta ambas alertas en un solo diccionario, ideal para
    mostrar en la pantalla principal del Administrador.
    """
    return {
        "alertas_stock": verificar_stock_bajo(),
        "alertas_vencimiento": verificar_vencimientos_proximos()
    }


# ==========================================
# PRUEBAS EN CONSOLA
# ==========================================
if __name__ == "__main__":
    print("=== DASHBOARD DE ALERTAS AUTOMÁTICAS ===\n")
    
    reporte = obtener_dashboard_alertas()
    
    print("--- 1. Alertas de Reabastecimiento (Stock Bajo) ---")
    if not reporte["alertas_stock"]:
        print("✅ Inventario sano. Ningún producto por debajo del mínimo.")
    else:
        for alerta in reporte["alertas_stock"]:
            print(f"⚠️ [{alerta['estado']}] {alerta['producto']}: Quedan {alerta['stock_actual']} (Mínimo: {alerta['stock_minimo']})")
            
    print("\n--- 2. Alertas de Caducidad (Próximos 90 días) ---")
    if not reporte["alertas_vencimiento"]:
        print("✅ No hay lotes próximos a vencer.")
    else:
        for alerta in reporte["alertas_vencimiento"]:
            if "VENCIDO" in alerta["estado"]:
                print(f"❌ [{alerta['estado']}] {alerta['producto']} (Lote: {alerta['lote']}) - {alerta['cantidad']} cajas.")
            else:
                print(f"⚠️ [{alerta['estado']}] {alerta['producto']} (Lote: {alerta['lote']}) - {alerta['cantidad']} cajas.")