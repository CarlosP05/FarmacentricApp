# Importamos los expedientes de los empleados desde nuestra carpeta de datos
from Datos.datos_rrhh import empleados

# Constantes de deducciones de ley 
TASA_INSS_LABORAL = 0.07  # 7% de retención al empleado

def calcular_pago_individual(id_empleado):
    """
    Toma el salario base de un empleado, aplica las deducciones 
    y retorna su salario neto a recibir.
    """
    for empleado in empleados:
        if empleado["id_empleado"] == id_empleado:
            salario_bruto = empleado["salario_base"]
            
            # Cálculo de deducciones
            deduccion_inss = salario_bruto * TASA_INSS_LABORAL
            
            # Salario final que se le transfiere al trabajador
            salario_neto = salario_bruto - deduccion_inss
            
            return {
                "exito": True,
                "nombre": empleado["nombre_completo"],
                "cargo": empleado["cargo"],
                "desglose": {
                    "salario_bruto": salario_bruto,
                    "deduccion_inss": deduccion_inss,
                    "salario_neto": salario_neto
                }
            }
            
    return {
        "exito": False, 
        "mensaje": f"Error: No se encontró al empleado con ID {id_empleado}."
    }

def procesar_nomina_general():
    """
    Calcula el pago de todos los empleados activos y devuelve 
    el total de dinero que la farmacia necesita desembolsar.
    """
    detalle_nomina = []
    desembolso_total_neto = 0.0
    desembolso_total_inss = 0.0
    
    for empleado in empleados:
        resultado = calcular_pago_individual(empleado["id_empleado"])
        
        if resultado["exito"]:
            detalle_nomina.append(resultado)
            desembolso_total_neto += resultado["desglose"]["salario_neto"]
            desembolso_total_inss += resultado["desglose"]["deduccion_inss"]
            
    return {
        "cantidad_empleados": len(detalle_nomina),
        "detalle": detalle_nomina,
        "totales_empresa": {
            "pago_neto_empleados": desembolso_total_neto,
            "pago_inss_retencion": desembolso_total_inss,
            "costo_total_nomina": desembolso_total_neto + desembolso_total_inss
        }
    }


# ==========================================
# PRUEBAS EN CONSOLA
# ==========================================
if __name__ == "__main__":
    print("=== PROCESAMIENTO DE NÓMINA - FARMACENTRIC ===\n")
    
    # El Contador presiona el botón "Calcular Nómina del Mes"
    reporte_nomina = procesar_nomina_general()
    
    print(f"Empleados procesados: {reporte_nomina['cantidad_empleados']}")
    print("-" * 40)
    
    # Imprimiendo las colillas de pago individuales
    for pago in reporte_nomina["detalle"]:
        print(f"Empleado: {pago['nombre']} ({pago['cargo']})")
        print(f"  + Salario Bruto: C$ {pago['desglose']['salario_bruto']:.2f}")
        print(f"  - INSS (7%):     C$ {pago['desglose']['deduccion_inss']:.2f}")
        print(f"  = NETO A PAGAR:  C$ {pago['desglose']['salario_neto']:.2f}")
        print("-" * 40)
        
    # Lo que le importa al Administrador
    print("\nRESUMEN PARA FINANZAS:")
    print(f"Total a transferir a empleados: C$ {reporte_nomina['totales_empresa']['pago_neto_empleados']:.2f}")
    print(f"Total a reportar al seguro:     C$ {reporte_nomina['totales_empresa']['pago_inss_retencion']:.2f}")
    print(f"Gasto Total de la Nómina:       C$ {reporte_nomina['totales_empresa']['costo_total_nomina']:.2f}")