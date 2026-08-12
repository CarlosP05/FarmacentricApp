# Catálogo general de productos
catalogo_productos = [
    {
        "id_producto": 1001,
        "nombre": "Paracetamol 500mg",
        "categoria": "Venta Libre",
        "precio_venta": 85.50,
        "stock_minimo": 50, # Nivel para disparar la alerta de reabastecimiento
        "requiere_receta": False
    },
    {
        "id_producto": 1002,
        "nombre": "Amoxicilina 875mg",
        "categoria": "Antibiótico",
        "precio_venta": 320.00,
        "stock_minimo": 20,
        "requiere_receta": True
    },
    {
        "id_producto": 1003,
        "nombre": "Diazepam 5mg",
        "categoria": "Controlado",
        "precio_venta": 450.00,
        "stock_minimo": 10,
        "requiere_receta": True
    }
]

# Detalle de lotes físicos en la farmacia (Aquí calcularemos las caducidades y el stock real)
lotes_inventario = [
    {
        "id_lote": "L-2026-001",
        "id_producto": 1001,
        "cantidad_actual": 80,
        "fecha_vencimiento": "2027-12-31" 
    },
    {
        "id_lote": "L-2026-002",
        "id_producto": 1001,
        "cantidad_actual": 10,
        "fecha_vencimiento": "2026-09-15" # Próximo a vencer
    },
    {
        "id_lote": "L-2026-003",
        "id_producto": 1002,
        "cantidad_actual": 15, # Por debajo del stock mínimo (20)
        "fecha_vencimiento": "2028-05-20"
    },
    {
        "id_lote": "L-2026-004",
        "id_producto": 1003,
        "cantidad_actual": 25,
        "fecha_vencimiento": "2027-01-10"
    }
]