# Diccionario de roles para evitar errores tipográficos en la lógica
ROLES = {
    "ADMIN": "Administrador",
    "RRHH": "Contador/RRHH",
    "CAJERO": "Cajero/Farmacéutico"
}

# Simulando la tabla de Usuarios
usuarios = [
    {
        "id_usuario": 1,
        "username": "cpalma",
        "password": "admin123", # En un sistema real esto iría encriptado
        "rol": ROLES["ADMIN"],
        "activo": True
    },
    {
        "id_usuario": 2,
        "username": "mcontable",
        "password": "rrhh123",
        "rol": ROLES["RRHH"],
        "activo": True
    },
    {
        "id_usuario": 3,
        "username": "jventas",
        "password": "caja123",
        "rol": ROLES["CAJERO"],
        "activo": True
    }
]