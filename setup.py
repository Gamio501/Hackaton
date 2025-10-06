#!/usr/bin/env python
"""
Script de configuración inicial para el Sistema de Pronóstico del Clima
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Función principal de configuración"""
    print("🌤️ Sistema de Pronóstico del Clima - Configuración Inicial")
    print("=" * 60)
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detectado")
    
    # Crear entorno virtual si no existe
    if not os.path.exists("venv"):
        if not run_command("python -m venv venv", "Creando entorno virtual"):
            sys.exit(1)
    else:
        print("✅ Entorno virtual ya existe")
    
    # Activar entorno virtual e instalar dependencias
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Linux/Mac
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Instalar dependencias
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Instalando dependencias"):
        sys.exit(1)
    
    # Crear migraciones
    if not run_command("python manage.py makemigrations", "Creando migraciones"):
        sys.exit(1)
    
    # Aplicar migraciones
    if not run_command("python manage.py migrate", "Aplicando migraciones"):
        sys.exit(1)
    
    # Crear superusuario (opcional)
    print("\n🔐 ¿Deseas crear un superusuario para el admin? (y/n): ", end="")
    create_superuser = input().lower().strip()
    
    if create_superuser in ['y', 'yes', 's', 'si', 'sí']:
        run_command("python manage.py createsuperuser", "Creando superusuario")
    
    print("\n" + "=" * 60)
    print("🎉 ¡Configuración completada exitosamente!")
    print("\n📋 Próximos pasos:")
    print("1. Activar entorno virtual:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Ejecutar servidor:")
    print("   python manage.py runserver")
    print("3. Abrir navegador en: http://127.0.0.1:8000")
    print("\n🌤️ ¡Disfruta tu Sistema de Pronóstico del Clima!")

if __name__ == "__main__":
    main()
