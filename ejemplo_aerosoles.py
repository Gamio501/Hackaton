#!/usr/bin/env python3
"""
Ejemplo de uso del módulo de parámetros de aerosoles y polvo atmosférico
Integrado en el sistema de pronóstico climático Django
"""

import numpy as np
from clima.models import RegistroClima

def ejemplo_calculo_aerosoles():
    """
    Ejemplo completo de cálculo de parámetros de aerosoles
    """
    print("=" * 60)
    print("EJEMPLO DE CÁLCULO DE PARÁMETROS DE AEROSOLES")
    print("=" * 60)
    
    # Crear un registro de clima de ejemplo
    registro = RegistroClima(
        temperatura=25.5,
        humedad=65.0,
        presion=1013.25,
        velocidad_viento=15.0,
        altura=100.0,
        nubosidad=30.0,
        latitud=40.4168,
        longitud=-3.7038
    )
    
    print(f"📍 Ubicación: Madrid, España")
    print(f"🌡️  Temperatura: {registro.temperatura}°C")
    print(f"💧 Humedad: {registro.humedad}%")
    print(f"🌬️  Viento: {registro.velocidad_viento} km/h")
    print()
    
    # Ejemplo 1: Datos simulados
    print("📊 CÁLCULO CON DATOS SIMULADOS:")
    print("-" * 40)
    
    # Calcular todos los parámetros con datos simulados
    registro.calcular_todos_parametros_aerosoles()
    
    # Mostrar resultados
    resumen = registro.obtener_resumen_aerosoles()
    for parametro, valor in resumen.items():
        print(f"  {parametro.replace('_', ' ').title()}: {valor}")
    
    print()
    
    # Ejemplo 2: Datos reales simulados
    print("📊 CÁLCULO CON DATOS REALES SIMULADOS:")
    print("-" * 40)
    
    # Generar datos más realistas
    np.random.seed(123)  # Para reproducibilidad
    
    # Simular mediciones de partículas
    n_particulas = 5000
    diametros = np.random.lognormal(mean=0.5, sigma=0.8, size=n_particulas)
    masas = np.random.lognormal(mean=1.5, sigma=0.4, size=n_particulas)
    numeros = np.random.poisson(lam=3, size=n_particulas)
    
    # Perfil vertical de temperatura
    alturas = np.linspace(0, 3000, 30)
    temperaturas = registro.temperatura - 0.0065 * alturas  # Gradiente adiabático
    
    # Perfil de viento
    velocidades_u = 5 + 2 * np.sin(alturas / 1000) + np.random.normal(0, 1, len(alturas))
    velocidades_v = 3 + 1 * np.cos(alturas / 1000) + np.random.normal(0, 0.5, len(alturas))
    
    # Coeficientes de extinción (simulados)
    coeficientes_extincion = 0.0008 * np.exp(-alturas / 1500) + 0.0002
    
    # Datos reales simulados
    datos_reales = {
        'diametros': diametros.tolist(),
        'masas': masas.tolist(),
        'numeros': numeros.tolist(),
        'volumen_aire': 2.0,  # m³
        'alturas': alturas.tolist(),
        'coeficientes_extincion': coeficientes_extincion.tolist(),
        'temperaturas': temperaturas.tolist(),
        'velocidades_u': velocidades_u.tolist(),
        'velocidades_v': velocidades_v.tolist()
    }
    
    # Calcular con datos reales
    registro.calcular_todos_parametros_aerosoles(datos_reales)
    
    # Mostrar resultados
    resumen_real = registro.obtener_resumen_aerosoles()
    for parametro, valor in resumen_real.items():
        print(f"  {parametro.replace('_', ' ').title()}: {valor}")
    
    print()
    
    # Ejemplo 3: Cálculos individuales
    print("🔬 CÁLCULOS INDIVIDUALES:")
    print("-" * 40)
    
    # Densidad del polvo
    masa_total = sum(masas)
    volumen = 2.0
    densidad = registro.calcular_densidad_polvo(masa_total, volumen)
    print(f"  Densidad del polvo: {densidad} µg/m³")
    
    # PM2.5 y PM10
    pm25 = registro.calcular_pm(diametros.tolist(), masas.tolist(), volumen, 2.5)
    pm10 = registro.calcular_pm(diametros.tolist(), masas.tolist(), volumen, 10.0)
    print(f"  PM2.5: {pm25} µg/m³")
    print(f"  PM10: {pm10} µg/m³")
    
    # Distribución de tamaño
    diam_medio, desv_diam = registro.calcular_distribucion_tamano(
        diametros.tolist(), numeros.tolist()
    )
    print(f"  Diámetro medio: {diam_medio} µm")
    print(f"  Desviación estándar: {desv_diam} µm")
    
    # AOD
    aod = registro.calcular_aod(coeficientes_extincion.tolist(), alturas.tolist())
    print(f"  AOD: {aod}")
    
    # Visibilidad
    coef_ext_promedio = np.mean(coeficientes_extincion)
    visibilidad = registro.calcular_visibilidad(coef_ext_promedio)
    print(f"  Visibilidad: {visibilidad} km")
    
    # Altura de capa de mezcla
    altura_capa = registro.calcular_altura_capa_mezcla(
        temperaturas.tolist(), alturas.tolist(), 
        velocidades_u.tolist(), velocidades_v.tolist()
    )
    print(f"  Altura capa mezcla: {altura_capa} m")
    
    print()
    
    # Ejemplo 4: Análisis de calidad del aire
    print("🌍 ANÁLISIS DE CALIDAD DEL AIRE:")
    print("-" * 40)
    
    # Clasificación PM2.5 (OMS)
    if pm25 < 15:
        calidad_pm25 = "Buena"
    elif pm25 < 35:
        calidad_pm25 = "Moderada"
    elif pm25 < 55:
        calidad_pm25 = "Insalubre para grupos sensibles"
    else:
        calidad_pm25 = "Insalubre"
    
    # Clasificación PM10 (OMS)
    if pm10 < 25:
        calidad_pm10 = "Buena"
    elif pm10 < 50:
        calidad_pm10 = "Moderada"
    elif pm10 < 90:
        calidad_pm10 = "Insalubre para grupos sensibles"
    else:
        calidad_pm10 = "Insalubre"
    
    # Clasificación AOD
    if aod < 0.1:
        aod_categoria = "Muy limpio"
    elif aod < 0.3:
        aod_categoria = "Limpio"
    elif aod < 0.5:
        aod_categoria = "Moderado"
    else:
        aod_categoria = "Contaminado"
    
    print(f"  PM2.5: {pm25:.2f} µg/m³ - {calidad_pm25}")
    print(f"  PM10: {pm10:.2f} µg/m³ - {calidad_pm10}")
    print(f"  AOD: {aod:.4f} - {aod_categoria}")
    print(f"  Visibilidad: {visibilidad:.1f} km")
    
    if visibilidad < 5:
        print("  ⚠️  Visibilidad reducida - Precaución al conducir")
    elif visibilidad < 10:
        print("  ⚠️  Visibilidad moderada")
    else:
        print("  ✅ Visibilidad excelente")
    
    print()
    
    # Ejemplo 5: Fórmulas implementadas
    print("📐 FÓRMULAS IMPLEMENTADAS:")
    print("-" * 40)
    print("1. Densidad del polvo: ρ_polvo = M / V")
    print("2. PM2.5/PM10: PM_x = Σ(d_i ≤ x) M_i / V")
    print("3. Diámetro medio: d̄ = Σ(n_i * d_i) / Σ(n_i)")
    print("4. Desviación estándar: σ = √(Σ(n_i * (d_i - d̄)²) / Σ(n_i))")
    print("5. AOD: AOD = ∫₀^∞ α_ext(z) dz")
    print("6. Visibilidad: Vis = 3.912 / β_ext")
    print("7. Altura capa mezcla: Ri = (g/θ) * (Δθ * Δz) / (Δu² + Δv²)")
    
    print()
    print("=" * 60)
    print("✅ EJEMPLO COMPLETADO")
    print("=" * 60)

if __name__ == "__main__":
    ejemplo_calculo_aerosoles()

