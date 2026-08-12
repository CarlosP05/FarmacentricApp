# Importamos nuestra "tabla" de usuarios desde el archivo de datos
# (En la práctica real, asegúrate de que ambos archivos estén en la misma carpeta)
from Datos.datos_usuarios import usuarios

def iniciar_sesion(username, password): 
    """
    Verifica las credenciales del usuario y retorna un diccionario con el resultado.
    
    Retorna:
    - exito (bool): True si las credenciales son correctas, False si no.
    - mensaje (str): Un mensaje descriptivo para mostrar en la interfaz.
    - datos_usuario (dict o None): La información del usuario si el login es exitoso.
    """
    
    # Recorremos nuestra lista estática de usuarios
    for usuario in usuarios:
        # Validamos si coincide el usuario y la contraseña
        if usuario["username"] == username and usuario["password"] == password:
            
            # Verificamos si el usuario está activo (medida de seguridad básica)
            if not usuario["activo"]:
                return {
                    "exito": False,
                    "mensaje": "Error: Este usuario está desactivado. Contacte al administrador.",
                    "datos_usuario": None
                }
            
            # Si todo está correcto, devolvemos éxito y los datos
            return {
                "exito": True,
                "mensaje": f"Inicio de sesión exitoso. Rol detectado: {usuario['rol']}",
                "datos_usuario": usuario
            }
            
    # Si el ciclo termina y no encontró coincidencias
    return {
        "exito": False,
        "mensaje": "Error: Usuario o contraseña incorrectos.",
        "datos_usuario": None
    }


# ==========================================
# PRUEBAS EN CONSOLA (Sin interfaz gráfica)
# ==========================================
if __name__ == "__main__":
    # Prueba 1: Login exitoso como Administrador
    print("--- Prueba 1 ---")
    resultado1 = iniciar_sesion("cpalma", "admin123")
    print(resultado1["mensaje"])
    if resultado1["exito"]:
        print(f"Abriendo el Dashboard de: {resultado1['datos_usuario']['rol']}")

    # Prueba 2: Contraseña incorrecta
    print("\n--- Prueba 2 ---")
    resultado2 = iniciar_sesion("mcontable", "clave_equivocada")
    print(resultado2["mensaje"])

    # Prueba 3: Usuario inexistente
    print("\n--- Prueba 3 ---")
    resultado3 = iniciar_sesion("desconocido", "12345")
    print(resultado3["mensaje"])