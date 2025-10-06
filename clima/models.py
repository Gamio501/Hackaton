from django.db import models
import math
import numpy as np

class RegistroClima(models.Model):
    temperatura = models.FloatField(help_text="Temperatura en grados Celsius")
    humedad = models.FloatField(help_text="Humedad relativa en porcentaje (0-100)")
    presion = models.FloatField(help_text="Presión atmosférica en hPa")
    velocidad_viento = models.FloatField(help_text="Velocidad del viento en km/h")
    altura = models.FloatField(help_text="Altura sobre el nivel del mar en metros")
    nubosidad = models.FloatField(help_text="Nubosidad en porcentaje (0-100)")
    latitud = models.FloatField(help_text="Latitud en grados decimales")
    longitud = models.FloatField(help_text="Longitud en grados decimales")
    nombre_lugar = models.CharField(max_length=200, blank=True, help_text="Nombre del lugar donde se realizó el cálculo")
    
    # Parámetros de polvo atmosférico y aerosoles
    densidad_polvo = models.FloatField(default=0.0, help_text="Densidad del polvo en µg/m³")
    pm25 = models.FloatField(default=0.0, help_text="PM2.5 en µg/m³")
    pm10 = models.FloatField(default=0.0, help_text="PM10 en µg/m³")
    diametro_medio = models.FloatField(default=0.0, help_text="Diámetro medio de partículas en µm")
    desviacion_diametro = models.FloatField(default=0.0, help_text="Desviación estándar del diámetro en µm")
    aod = models.FloatField(default=0.0, help_text="Profundidad óptica de aerosoles (AOD)")
    visibilidad = models.FloatField(default=0.0, help_text="Visibilidad atmosférica en km")
    altura_capa_mezcla = models.FloatField(default=0.0, help_text="Altura de la capa de mezcla en metros")
    
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Clima del {self.fecha:%Y-%m-%d %H:%M}"

    def calcular_indice_calor(self):
        """Calcula el índice de calor (Heat Index)"""
        t = self.temperatura
        h = self.humedad / 100
        
        # Fórmula del índice de calor
        hi = -8.78469475556 + 1.61139411 * t + 2.33854883889 * h + \
             -0.14611605 * t * h + -0.012308094 * (t**2) + \
             -0.0164248277778 * (h**2) + 0.002211732 * (t**2) * h + \
             0.00072546 * t * (h**2) + -0.000003582 * (t**2) * (h**2)
        
        return round(hi, 2)

    def calcular_sensacion_termica(self):
        """Calcula la sensación térmica (Wind Chill)"""
        t = self.temperatura
        v = self.velocidad_viento * 0.277778  # Convertir km/h a m/s
        
        if t <= 10 and v >= 4.8:
            # Fórmula de sensación térmica
            wc = 13.12 + 0.6215 * t - 11.37 * (v**0.16) + 0.3965 * t * (v**0.16)
            return round(wc, 2)
        else:
            return t

    def calcular_punto_rocio(self):
        """Calcula el punto de rocío"""
        t = self.temperatura
        h = self.humedad
        
        # Fórmula de Magnus
        a = 17.27
        b = 237.7
        alpha = ((a * t) / (b + t)) + math.log(h / 100)
        dp = (b * alpha) / (a - alpha)
        
        return round(dp, 2)

    def calcular_presion_ajustada(self):
        """Calcula la presión ajustada al nivel del mar"""
        p = self.presion
        h = self.altura
        
        # Fórmula barométrica
        p0 = p * math.exp(h / 8434.5)
        return round(p0, 2)

    def pronosticar_tiempo(self):
        """Pronostica el tiempo basado en los parámetros"""
        pronostico = {
            'condicion': '',
            'descripcion': '',
            'probabilidad_lluvia': 0,
            'recomendaciones': []
        }
        
        # Análisis de humedad y nubosidad para probabilidad de lluvia
        prob_lluvia = 0
        
        # Factor de humedad (0-40 puntos)
        if self.humedad > 90:
            prob_lluvia += 40
        elif self.humedad > 80:
            prob_lluvia += 30
        elif self.humedad > 70:
            prob_lluvia += 20
        elif self.humedad > 60:
            prob_lluvia += 10
        
        # Factor de nubosidad (0-30 puntos)
        if self.nubosidad > 90:
            prob_lluvia += 30
        elif self.nubosidad > 80:
            prob_lluvia += 25
        elif self.nubosidad > 70:
            prob_lluvia += 20
        elif self.nubosidad > 50:
            prob_lluvia += 15
        elif self.nubosidad > 30:
            prob_lluvia += 10
        
        # Factor de presión (0-20 puntos)
        if self.presion < 1000:
            prob_lluvia += 20
        elif self.presion < 1010:
            prob_lluvia += 15
        elif self.presion < 1020:
            prob_lluvia += 10
        
        # Factor de viento (0-10 puntos)
        if self.velocidad_viento > 30:
            prob_lluvia += 10
        elif self.velocidad_viento > 20:
            prob_lluvia += 5
        
        # Asegurar que esté entre 0 y 100
        prob_lluvia = max(0, min(100, prob_lluvia))
        
        pronostico['probabilidad_lluvia'] = prob_lluvia
        
        # Actualizar condición basada en probabilidad
        if prob_lluvia > 70:
            pronostico['condicion'] = 'Lluvioso'
            pronostico['descripcion'] = 'Alta probabilidad de precipitaciones'
        elif prob_lluvia > 40:
            pronostico['condicion'] = 'Nublado'
            pronostico['descripcion'] = 'Posibilidad de lluvias'
        elif prob_lluvia > 20:
            pronostico['condicion'] = 'Parcialmente nublado'
            pronostico['descripcion'] = 'Algunas nubes dispersas'
        else:
            pronostico['condicion'] = 'Despejado'
            pronostico['descripcion'] = 'Cielo despejado con buena visibilidad'
        
        # Análisis de viento
        if self.velocidad_viento > 50:
            pronostico['recomendaciones'].append('Viento fuerte - Evitar actividades al aire libre')
        elif self.velocidad_viento > 30:
            pronostico['recomendaciones'].append('Viento moderado - Tener precaución')
        
        # Análisis de temperatura
        if self.temperatura > 35:
            pronostico['recomendaciones'].append('Temperatura alta - Mantenerse hidratado')
        elif self.temperatura < 0:
            pronostico['recomendaciones'].append('Temperatura baja - Abrigarse bien')
        
        return pronostico

    def calcular_estacion(self):
        """Determina la estación del año basada en la latitud y fecha"""
        mes = self.fecha.month
        
        # Para el hemisferio norte (latitud positiva)
        if self.latitud > 0:
            if mes in [12, 1, 2]:
                return "Invierno"
            elif mes in [3, 4, 5]:
                return "Primavera"
            elif mes in [6, 7, 8]:
                return "Verano"
            else:
                return "Otoño"
        # Para el hemisferio sur (latitud negativa)
        else:
            if mes in [12, 1, 2]:
                return "Verano"
            elif mes in [3, 4, 5]:
                return "Otoño"
            elif mes in [6, 7, 8]:
                return "Invierno"
            else:
                return "Primavera"
    
    # ========================================
    # MÉTODOS PARA PARÁMETROS DE AEROSOLES
    # ========================================
    
    def calcular_densidad_polvo(self, masa_particulas, volumen_aire):
        """
        Calcula la densidad del polvo atmosférico
        
        Fórmula: ρ_polvo = M / V
        Donde:
        - M = masa de partículas (µg)
        - V = volumen de aire muestreado (m³)
        - Resultado en µg/m³
        """
        if volumen_aire <= 0:
            return 0.0
        return round(masa_particulas / volumen_aire, 3)
    
    def calcular_pm(self, diametros, masas, volumen_aire, limite_diametro):
        """
        Calcula PM2.5 o PM10
        
        Fórmula: PM_x = Σ(d_i ≤ x) M_i / V
        Donde:
        - d_i = diámetro de partícula
        - x = 2.5 o 10 µm
        - M_i = masa de partículas en ese rango
        - V = volumen de aire muestreado (m³)
        """
        if volumen_aire <= 0:
            return 0.0
        
        # Filtrar partículas menores o iguales al límite
        indices = np.where(np.array(diametros) <= limite_diametro)[0]
        masa_total = sum(masas[i] for i in indices)
        
        return round(masa_total / volumen_aire, 3)
    
    def calcular_distribucion_tamano(self, diametros, numeros_particulas):
        """
        Calcula la distribución de tamaño (media y desviación)
        
        Fórmulas:
        - d̄ = Σ(n_i * d_i) / Σ(n_i)
        - σ = √(Σ(n_i * (d_i - d̄)²) / Σ(n_i))
        Donde:
        - n_i = número de partículas
        - d_i = diámetro de partícula
        """
        if len(diametros) == 0 or sum(numeros_particulas) == 0:
            return 0.0, 0.0
        
        diametros = np.array(diametros)
        numeros = np.array(numeros_particulas)
        
        # Diámetro medio
        diametro_medio = np.sum(numeros * diametros) / np.sum(numeros)
        
        # Desviación estándar
        desviacion = np.sqrt(np.sum(numeros * (diametros - diametro_medio)**2) / np.sum(numeros))
        
        return round(diametro_medio, 3), round(desviacion, 3)
    
    def calcular_aod(self, coeficientes_extincion, alturas):
        """
        Calcula la profundidad óptica de aerosoles (AOD)
        
        Fórmula: AOD = ∫₀^∞ α_ext(z) dz
        Donde:
        - α_ext = coeficiente de extinción (absorción + dispersión)
        - z = altura
        """
        if len(coeficientes_extincion) != len(alturas) or len(coeficientes_extincion) < 2:
            return 0.0
        
        # Integración trapezoidal
        aod = np.trapz(coeficientes_extincion, alturas)
        return round(aod, 6)
    
    def calcular_visibilidad(self, coeficiente_extincion):
        """
        Calcula la visibilidad atmosférica usando la Ley de Koschmieder
        
        Fórmula: Vis = 3.912 / β_ext
        Donde:
        - β_ext = coeficiente de extinción (m⁻¹)
        """
        if coeficiente_extincion <= 0:
            return float('inf')
        
        visibilidad = 3.912 / coeficiente_extincion
        return round(visibilidad / 1000, 3)  # Convertir a km
    
    def calcular_altura_capa_mezcla(self, temperaturas, alturas, velocidades_u, velocidades_v):
        """
        Calcula la altura de la capa de mezcla usando el criterio de Richardson
        
        Fórmula: Ri = (g/θ) * (Δθ * Δz) / (Δu² + Δv²)
        Si Ri < 0.25, el flujo es turbulento y esa es la altura de la capa de mezcla
        """
        if len(temperaturas) < 2 or len(alturas) < 2:
            return 0.0
        
        g = 9.81  # Aceleración de la gravedad
        altura_capa = 0.0
        
        for i in range(1, len(temperaturas)):
            # Temperatura potencial (aproximación)
            theta_i = temperaturas[i] + 0.0098 * alturas[i]
            theta_0 = temperaturas[0] + 0.0098 * alturas[0]
            
            delta_theta = theta_i - theta_0
            delta_z = alturas[i] - alturas[0]
            
            if i < len(velocidades_u) and i < len(velocidades_v):
                delta_u = velocidades_u[i] - velocidades_u[0]
                delta_v = velocidades_v[i] - velocidades_v[0]
                velocidad_cuadrada = delta_u**2 + delta_v**2
            else:
                velocidad_cuadrada = 1.0  # Valor por defecto
            
            if velocidad_cuadrada > 0:
                ri = (g / theta_0) * (delta_theta * delta_z) / velocidad_cuadrada
                
                if ri < 0.25:
                    altura_capa = alturas[i]
                else:
                    break
        
        return round(altura_capa, 2)
    
    def calcular_todos_parametros_aerosoles(self, datos_particulas=None):
        """
        Calcula todos los parámetros de aerosoles con datos simulados o reales
        
        Args:
            datos_particulas: Diccionario con datos reales, si no se proporciona usa datos simulados
        """
        if datos_particulas is None:
            # Generar datos simulados para demostración
            np.random.seed(42)  # Para reproducibilidad
            
            # Simular 1000 partículas
            n_particulas = 1000
            diametros = np.random.lognormal(mean=1.0, sigma=0.5, size=n_particulas)
            masas = np.random.lognormal(mean=2.0, sigma=0.3, size=n_particulas)
            numeros = np.random.poisson(lam=5, size=n_particulas)
            
            # Volumen de aire muestreado (m³)
            volumen_aire = 1.0
            
            # Coeficientes de extinción simulados
            alturas = np.linspace(0, 2000, 20)
            coeficientes_extincion = np.exp(-alturas/1000) * 0.001
            
        else:
            # Usar datos proporcionados
            diametros = datos_particulas.get('diametros', [])
            masas = datos_particulas.get('masas', [])
            numeros = datos_particulas.get('numeros', [])
            volumen_aire = datos_particulas.get('volumen_aire', 1.0)
            alturas = datos_particulas.get('alturas', np.linspace(0, 2000, 20))
            coeficientes_extincion = datos_particulas.get('coeficientes_extincion', np.exp(-alturas/1000) * 0.001)
        
        # Calcular todos los parámetros
        self.densidad_polvo = self.calcular_densidad_polvo(sum(masas), volumen_aire)
        self.pm25 = self.calcular_pm(diametros, masas, volumen_aire, 2.5)
        self.pm10 = self.calcular_pm(diametros, masas, volumen_aire, 10.0)
        
        diam_medio, desv_diam = self.calcular_distribucion_tamano(diametros, numeros)
        self.diametro_medio = diam_medio
        self.desviacion_diametro = desv_diam
        
        self.aod = self.calcular_aod(coeficientes_extincion, alturas)
        
        # Coeficiente de extinción promedio para visibilidad
        coef_ext_promedio = np.mean(coeficientes_extincion)
        self.visibilidad = self.calcular_visibilidad(coef_ext_promedio)
        
        # Simular datos para altura de capa de mezcla
        if datos_particulas is None:
            temperaturas = self.temperatura - 0.0065 * alturas  # Gradiente adiabático
            velocidades_u = np.random.normal(5, 2, len(alturas))
            velocidades_v = np.random.normal(3, 1, len(alturas))
        else:
            temperaturas = datos_particulas.get('temperaturas', [self.temperatura] * len(alturas))
            velocidades_u = datos_particulas.get('velocidades_u', [5] * len(alturas))
            velocidades_v = datos_particulas.get('velocidades_v', [3] * len(alturas))
        
        self.altura_capa_mezcla = self.calcular_altura_capa_mezcla(
            temperaturas, alturas, velocidades_u, velocidades_v
        )
    
    def obtener_resumen_aerosoles(self):
        """
        Retorna un resumen de todos los parámetros de aerosoles calculados
        """
        return {
            'densidad_polvo': f"{self.densidad_polvo} µg/m³",
            'pm25': f"{self.pm25} µg/m³",
            'pm10': f"{self.pm10} µg/m³",
            'diametro_medio': f"{self.diametro_medio} µm",
            'desviacion_diametro': f"{self.desviacion_diametro} µm",
            'aod': f"{self.aod}",
            'visibilidad': f"{self.visibilidad} km",
            'altura_capa_mezcla': f"{self.altura_capa_mezcla} m"
        }

class Login(models.Model):
    """Modelo para almacenar credenciales de acceso a la parte científica"""
    username = models.CharField(max_length=50, unique=True, help_text="Nombre de usuario")
    password = models.CharField(max_length=100, help_text="Contraseña (hash)")
    email = models.EmailField(help_text="Correo electrónico")
    nombre_completo = models.CharField(max_length=100, help_text="Nombre completo del usuario")
    rol = models.CharField(max_length=50, default='investigador', help_text="Rol del usuario (investigador, admin)")
    activo = models.BooleanField(default=True, help_text="Usuario activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultimo_acceso = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombre_completo} ({self.username})"
    
    class Meta:
        verbose_name = "Login"
        verbose_name_plural = "Logins"
