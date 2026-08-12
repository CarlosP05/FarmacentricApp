from Datos.datos_inventario import catalogo_productos, lotes_inventario

def registrar_nuevo_producto(nombre, categoria, precio_venta, stock_minimo, requiere_receta):
    """
    Agrega un nuevo medicamento al catálogo general.
    Genera un ID automáticamente.
    """
    # 1. Validar que el producto no exista ya (para evitar duplicados)
    for producto in catalogo_productos:
        if producto["nombre"].lower() == nombre.lower():
            return {
                "exito": False,
                "mensaje": f"Error: El producto '{nombre}' ya existe en el catálogo."
            }
    
    # 2. Generar un nuevo ID automáticamente (buscamos el más alto y sumamos 1)
    if catalogo_productos:
        nuevo_id = max([p["id_producto"] for p in catalogo_productos]) + 1
    else:
        nuevo_id = 1000 # Caso de catálogo vacío
        
    # 3. Crear el diccionario del nuevo producto
    nuevo_producto = {
        "id_producto": nuevo_id,
        "nombre": nombre,
        "categoria": categoria,
        "precio_venta": precio_venta,
        "stock_minimo": stock_minimo,
        "requiere_receta": requiere_receta
    }
    
    # 4. Agregarlo a nuestra "base de datos" estática
    catalogo_productos.append(nuevo_producto)
    
    return {
        "exito": True,
        "mensaje": f"Éxito: '{nombre}' registrado en el catálogo con ID {nuevo_id}.",
        "id_generado": nuevo_id
    }

def registrar_nuevo_lote(id_producto, id_lote, cantidad, fecha_vencimiento):
    """
    Ingresa las existencias físicas de un producto (cajas reales).
    """
    # 1. Validar que el id_producto exista en el catálogo
    producto_existe = False
    for prod in catalogo_productos:
        if prod["id_producto"] == id_producto:
            producto_existe = True
            break
            
    if not producto_existe:
        return {
            "exito": False,
            "mensaje": f"Error: No se puede ingresar el lote. El producto con ID {id_producto} no existe."
        }
        
    # 2. Crear y registrar el lote
    nuevo_lote = {
        "id_lote": id_lote,
        "id_producto": id_producto,
        "cantidad_actual": cantidad,
        "fecha_vencimiento": fecha_vencimiento
    }
    
    lotes_inventario.append(nuevo_lote)
    
    return {
        "exito": True,
        "mensaje": f"Éxito: Lote {id_lote} registrado. {cantidad} unidades añadidas."
    }


# ==========================================
# PRUEBAS EN CONSOLA
# ==========================================
if __name__ == "__main__":
    print("--- 1. Registrando nuevo producto en el catálogo ---")
    resultado_cat = registrar_nuevo_producto(
        nombre="Ibuprofeno 400mg", 
        categoria="Venta Libre", 
        precio_venta=120.00, 
        stock_minimo=30, 
        requiere_receta=False
    )
    print(resultado_cat["mensaje"])
    
    if resultado_cat["exito"]:
        print("\n--- 2. Ingresando las cajas (Lote) del nuevo producto ---")
        id_nuevo = resultado_cat["id_generado"]
        
        # Simulamos que ingresamos 50 cajas que vencen en el 2028
        resultado_lote = registrar_nuevo_lote(
            id_producto=id_nuevo, 
            id_lote="L-2026-005", 
            cantidad=50, 
            fecha_vencimiento="2028-10-15"
        )
        print(resultado_lote["mensaje"])
        
    print("\n--- 3. Probando validación de duplicados ---")
    resultado_dup = registrar_nuevo_producto("Paracetamol 500mg", "Venta Libre", 85.50, 50, False)
    print(resultado_dup["mensaje"])