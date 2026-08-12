from logica.logica_pos import procesar_venta
from logica.logica_rrhh import procesar_nomina_general

# Usaremos una variable global sencilla para simular la "Caja Chica" o el "Flujo de Efectivo"
# En un sistema real, esto se leería de una tabla de transacciones en la base de datos.
flujo_efectivo = {
    "ingresos_ventas": 0.0,
    "gastos_nomina": 0.0,
    "gastos_caja_chica": 0.0
}

def registrar_ingreso_venta(total_venta):
    """Suma el dinero de una venta exitosa al flujo de efectivo."""
    flujo_efectivo["ingresos_ventas"] += total_venta
    return True

def registrar_gasto_caja_chica(concepto, monto):
    """
    Registra salidas de dinero menores (ej. compra de papelería, pago de agua).
    """
    if monto <= 0:
        return {"exito": False, "mensaje": "El monto debe ser mayor a cero."}
        
    flujo_efectivo["gastos_caja_chica"] += monto
    return {"exito": True, "mensaje": f"Gasto registrado: {concepto} por C$ {monto:.2f}"}

def ejecutar_pago_nomina_mensual():
    """
    Calcula la nómina y registra el gasto total en el flujo de efectivo.
    """
    reporte = procesar_nomina_general()
    total_gasto = reporte["totales_empresa"]["costo_total_nomina"]
    
    flujo_efectivo["gastos_nomina"] += total_gasto
    return {"exito": True, "mensaje": f"Nómina procesada y registrada como gasto: C$ {total_gasto:.2f}"}

def generar_reporte_financiero():
    """
    Calcula el balance general (Ingresos - Egresos).
    Esta es la función que alimentará los gráficos del Dashboard del Administrador.
    """
    ingresos = flujo_efectivo["ingresos_ventas"]
    egresos = flujo_efectivo["gastos_nomina"] + flujo_efectivo["gastos_caja_chica"]
    balance_neto = ingresos - egresos
    
    # Determinamos el estado de salud financiera
    if balance_neto > 0:
        estado = "RENTABLE (Superávit)"
    elif balance_neto < 0:
        estado = "PÉRDIDA (Déficit)"
    else:
        estado = "PUNTO DE EQUILIBRIO"
        
    return {
        "ingresos_totales": ingresos,
        "egresos_totales": egresos,
        "desglose_egresos": {
            "nomina": flujo_efectivo["gastos_nomina"],
            "caja_chica": flujo_efectivo["gastos_caja_chica"]
        },
        "balance_neto": balance_neto,
        "estado_financiero": estado
    }


# ==========================================
# PRUEBAS EN CONSOLA (Simulación de un mes)
# ==========================================
if __name__ == "__main__":
    print("=== SIMULADOR FINANCIERO - FARMACENTRIC ===\n")
    
    # 1. Simulamos algunas ventas en el POS
    print("Registrando ventas del día...")
    # Simulamos una venta grande para tener ingresos (100 cajas de Paracetamol y 50 de Diazepam)
    venta_simulada = procesar_venta([
        {"id_producto": 1001, "cantidad": 50}, 
        {"id_producto": 1003, "cantidad": 20}
    ])
    
    if venta_simulada["exito"]:
        registrar_ingreso_venta(venta_simulada["total_cobrado"])
        print(f"+ Venta registrada por: C$ {venta_simulada['total_cobrado']:.2f}")

    # 2. Simulamos gastos de Caja Chica (El contador compra papelería)
    print("\nRegistrando gastos operativos...")
    gasto = registrar_gasto_caja_chica("Compra de resmas de papel y tóner", 1500.00)
    print(f"- {gasto['mensaje']}")

    # 3. Llegó fin de mes, pagamos la nómina
    print("\nProcesando pago de planilla...")
    pago = ejecutar_pago_nomina_mensual()
    print(f"- {pago['mensaje']}")

    # 4. El Administrador revisa el Dashboard General
    print("\n" + "="*40)
    print("      REPORTE FINANCIERO CONSOLIDADO")
    print("="*40)
    
    reporte = generar_reporte_financiero()
    
    print(f"INGRESOS (Ventas):      C$ {reporte['ingresos_totales']:,.2f}")
    print(f"EGRESOS TOTALES:        C$ {reporte['egresos_totales']:,.2f}")
    print(f"  ├─ Nómina:            C$ {reporte['desglose_egresos']['nomina']:,.2f}")
    print(f"  └─ Caja Chica:        C$ {reporte['desglose_egresos']['caja_chica']:,.2f}")
    print("-" * 40)
    print(f"BALANCE NETO:           C$ {reporte['balance_neto']:,.2f}")
    print(f"ESTADO:                 {reporte['estado_financiero']}")
    print("="*40)