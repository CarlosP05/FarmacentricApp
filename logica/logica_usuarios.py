# logica/logica_usuarios.py

from Datos.datos_usuarios import usuarios, ROLES

def obtener_lista_usuarios():
    """Devuelve la lista actual de usuarios para mostrarla en pantalla."""
    return usuarios

def registrar_nuevo_usuario(username, password, rol_seleccionado):
    """
    Valida y registra un nuevo usuario en el sistema.
    """
    # 1. Validar que el usuario no exista
    for u in usuarios:
        if u["username"].lower() == username.lower():
            return {"exito": False, "mensaje": f"Error: El usuario '{username}' ya existe."}
            
    # 2. Generar un nuevo ID
    if usuarios:
        nuevo_id = max([u["id_usuario"] for u in usuarios]) + 1
    else:
        nuevo_id = 1
        
    # 3. Crear el registro
    nuevo_usuario = {
        "id_usuario": nuevo_id,
        "username": username,
        "password": password,
        "rol": rol_seleccionado,
        "activo": True
    }
    
    usuarios.append(nuevo_usuario)
    
    return {"exito": True, "mensaje": f"Usuario '{username}' creado exitosamente."}