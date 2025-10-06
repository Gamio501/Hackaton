#!/usr/bin/env python3
"""
Test simple de los parametros de aerosoles
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pronostico_clima.settings')
django.setup()

from clima.models import RegistroClima
import numpy as np

def test_aerosoles():
    print("Test de parametros de aerosoles")
    print("=" * 40)
    
    # Crear registro
    registro = RegistroClima(
        temperatura=25.0,
        humedad=60.0,
        presion=1013.0,
        velocidad_viento=10.0,
        altura=100.0,
        nubosidad=20.0,
        latitud=40.0,
        longitud=-3.0
    )
    
    # Calcular parametros
    registro.calcular_todos_parametros_aerosoles()
    
    # Mostrar resultados
    print(f"Densidad polvo: {registro.densidad_polvo} ug/m3")
    print(f"PM2.5: {registro.pm25} ug/m3")
    print(f"PM10: {registro.pm10} ug/m3")
    print(f"Diametro medio: {registro.diametro_medio} um")
    print(f"Desviacion: {registro.desviacion_diametro} um")
    print(f"AOD: {registro.aod}")
    print(f"Visibilidad: {registro.visibilidad} km")
    print(f"Altura capa mezcla: {registro.altura_capa_mezcla} m")
    
    print("\nTest completado exitosamente!")

if __name__ == "__main__":
    test_aerosoles()

