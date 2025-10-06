#!/usr/bin/env python
import os
import sys
import django
import hashlib

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pronostico_clima.settings')
django.setup()

from clima.models import Login

def create_test_user():
    """Crear usuario de prueba para el sistema de login"""
    
    # Datos del usuario de prueba
    username = "investigador"
    password = "123456"  # Contraseña simple para demo
    email = "investigador@clima.com"
    nombre_completo = "Dr. Investigador Meteorológico"
    rol = "investigador"
    
    # Crear hash de la contraseña
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # Verificar si el usuario ya existe
    if Login.objects.filter(username=username).exists():
        print(f"El usuario '{username}' ya existe.")
        return
    
    # Crear usuario
    usuario = Login.objects.create(
        username=username,
        password=password_hash,
        email=email,
        nombre_completo=nombre_completo,
        rol=rol
    )
    
    print(f"Usuario creado exitosamente:")
    print(f"- Usuario: {username}")
    print(f"- Contraseña: {password}")
    print(f"- Nombre: {nombre_completo}")
    print(f"- Email: {email}")
    print(f"- Rol: {rol}")
    print("\n¡Puedes usar estas credenciales para acceder al sistema!")

if __name__ == "__main__":
    create_test_user()
