import customtkinter as ctk
from logica.logica_rrhh import procesar_nomina_general
from logica.logica_finanzas import registrar_gasto_caja_chica, ejecutar_pago_nomina_mensual

class VistaRRHH(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Farmacentric - Recursos Humanos y Finanzas")
        self.geometry("900x600")
        self.minsize(800, 500)

        # Dividimos la pantalla en dos columnas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1) # Panel Nómina
        self.grid_columnconfigure(1, weight=1) # Panel Caja Chica

        self.crear_panel_nomina()
        self.crear_panel_gastos()

    def crear_panel_nomina(self):
        """Módulo para el pago de salarios a los trabajadores"""
        self.panel_izq = ctk.CTkFrame(self)
        self.panel_izq.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        ctk.CTkLabel(self.panel_izq, text="Procesamiento de Nómina", font=("Roboto", 20, "bold")).pack(pady=(20, 10))

        self.btn_calcular = ctk.CTkButton(self.panel_izq, text="Calcular y Pagar Nómina del Mes", font=("Roboto", 14, "bold"), command=self.procesar_pago)
        self.btn_calcular.pack(pady=15)

        # Caja de texto para mostrar las colillas de pago
        self.caja_nomina = ctk.CTkTextbox(self.panel_izq, width=350, height=350, font=("Courier", 13))
        self.caja_nomina.pack(pady=10, padx=20, fill="both", expand=True)
        self.caja_nomina.insert("0.0", "Presione el botón para procesar la nómina actual.")
        self.caja_nomina.configure(state="disabled")
        
        # Botón de Salir
        self.btn_salir = ctk.CTkButton(self.panel_izq, text="Cerrar Sesión", fg_color="#d32f2f", hover_color="#b71c1c", command=lambda: self.master.cerrar_sesion(self))
        self.btn_salir.pack(side="bottom", pady=20)

    def crear_panel_gastos(self):
        """Módulo para registrar gastos operativos"""
        self.panel_der = ctk.CTkFrame(self, fg_color="#f0f0f0")
        self.panel_der.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

        ctk.CTkLabel(self.panel_der, text="Registro de Caja Chica", font=("Roboto", 20, "bold"), text_color="black").pack(pady=(20, 10))

        self.entrada_concepto = ctk.CTkEntry(self.panel_der, placeholder_text="Concepto del Gasto (Ej. Papelería)", width=280)
        self.entrada_concepto.pack(pady=10)

        self.entrada_monto = ctk.CTkEntry(self.panel_der, placeholder_text="Monto en C$", width=280)
        self.entrada_monto.pack(pady=10)

        self.btn_gasto = ctk.CTkButton(self.panel_der, text="Registrar Gasto", command=self.registrar_gasto)
        self.btn_gasto.pack(pady=15)

        self.lbl_mensaje_gasto = ctk.CTkLabel(self.panel_der, text="", font=("Roboto", 12))
        self.lbl_mensaje_gasto.pack(pady=10)

    def procesar_pago(self):
        # 1. Ejecutamos el pago (que se registra como gasto en finanzas)
        ejecutar_pago_nomina_mensual()
        
        # 2. Obtenemos el detalle visual para imprimirlo en pantalla
        reporte = procesar_nomina_general()
        
        texto = "--- COLILLAS DE PAGO ---\n\n"
        for pago in reporte["detalle"]:
            texto += f"Empleado: {pago['nombre']}\n"
            texto += f"Cargo: {pago['cargo']}\n"
            texto += f"  Bruto: C$ {pago['desglose']['salario_bruto']:,.2f}\n"
            texto += f"  -INSS: C$ {pago['desglose']['deduccion_inss']:,.2f}\n"
            texto += f"  NETO:  C$ {pago['desglose']['salario_neto']:,.2f}\n"
            texto += "-"*30 + "\n"
            
        texto += f"\nTOTAL DESEMBOLSADO: C$ {reporte['totales_empresa']['costo_total_nomina']:,.2f}"
        
        self.caja_nomina.configure(state="normal")
        self.caja_nomina.delete("0.0", "end")
        self.caja_nomina.insert("0.0", texto)
        self.caja_nomina.configure(state="disabled")
        
        # Desactivamos el botón para evitar que el contador pague la nómina dos veces por error
        self.btn_calcular.configure(state="disabled", text="Nómina Pagada")

    def registrar_gasto(self):
        concepto = self.entrada_concepto.get()
        monto_str = self.entrada_monto.get()
        
        if not concepto or not monto_str:
            self.lbl_mensaje_gasto.configure(text="Complete todos los campos.", text_color="red")
            return
            
        try:
            monto = float(monto_str)
            resultado = registrar_gasto_caja_chica(concepto, monto)
            
            if resultado["exito"]:
                self.lbl_mensaje_gasto.configure(text=f"✅ {resultado['mensaje']}", text_color="green")
                self.entrada_concepto.delete(0, 'end')
                self.entrada_monto.delete(0, 'end')
            else:
                self.lbl_mensaje_gasto.configure(text=resultado["mensaje"], text_color="red")
        except ValueError:
            self.lbl_mensaje_gasto.configure(text="El monto debe ser un número válido.", text_color="red")