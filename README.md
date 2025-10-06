# 🌤️ Sistema de Pronóstico del Clima

Una aplicación web desarrollada en Django para pronosticar el clima utilizando fórmulas meteorológicas avanzadas. Permite ingresar datos manualmente y obtener pronósticos detallados basados en cálculos científicos.

## 🚀 Características

- **Ingreso Manual de Datos**: Formulario intuitivo para ingresar parámetros meteorológicos
- **🗺️ Integración con Google Maps**: Selección visual de ubicación con mapa interactivo
- **Fórmulas Científicas**: Implementación de fórmulas meteorológicas reales
- **Pronósticos Detallados**: Análisis completo del clima con métricas avanzadas
- **Interfaz Moderna**: Diseño responsive con Bootstrap 5
- **Dashboard**: Estadísticas y análisis de datos históricos
- **API REST**: Endpoints para integración con otros sistemas

## 📊 Parámetros Meteorológicos

- **Temperatura** (°C): Temperatura del aire
- **Humedad Relativa** (%): Porcentaje de humedad en el aire
- **Presión Atmosférica** (hPa): Presión barométrica
- **Velocidad del Viento** (km/h): Velocidad del viento
- **Altura** (m): Altura sobre el nivel del mar
- **Nubosidad** (%): Porcentaje de cobertura nubosa
- **Coordenadas**: Latitud y longitud geográfica

## 🧮 Fórmulas Implementadas

### 1. Índice de Calor (Heat Index)
Calcula qué tan caliente se siente realmente cuando se combinan temperatura y humedad.

### 2. Sensación Térmica (Wind Chill)
Temperatura que siente el cuerpo humano considerando viento y temperatura.

### 3. Punto de Rocío
Temperatura a la cual el vapor de agua se condensa en agua líquida.

### 4. Presión Ajustada
Presión atmosférica ajustada al nivel del mar usando la fórmula barométrica.

### 5. Pronóstico del Tiempo
Análisis inteligente basado en todos los parámetros para determinar condiciones climáticas.

## 🛠️ Instalación

### Requisitos Previos
- Python 3.8+
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd pronostico-clima
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
```bash
# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Configurar base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor**
```bash
python manage.py runserver
```

8. **Acceder a la aplicación**
Abrir navegador en: `http://127.0.0.1:8000`

## 📱 Uso de la Aplicación

### 1. Ingresar Datos del Clima
- Navegar a la página principal
- **🗺️ Seleccionar Ubicación**: Usar el mapa interactivo o buscar una ubicación
- Completar el formulario con los parámetros meteorológicos
- Hacer clic en "Calcular Pronóstico"

### 2. Ver Pronóstico Detallado
- El sistema mostrará un análisis completo
- Métricas calculadas (índice de calor, sensación térmica, etc.)
- Recomendaciones basadas en las condiciones

### 3. Dashboard
- Ver estadísticas generales
- Análisis de datos históricos
- Último pronóstico registrado

### 4. Historial
- Lista de todos los registros
- Navegación por páginas
- Acceso rápido a pronósticos anteriores

## 🗺️ Integración con Google Maps

### Funcionalidades del Mapa
- **Búsqueda de Ubicaciones**: Campo de búsqueda con autocompletado
- **Selección Visual**: Clic en el mapa para seleccionar ubicación exacta
- **Marcador Arrastrable**: Ajustar la posición arrastrando el marcador
- **Coordenadas Automáticas**: Latitud y longitud se llenan automáticamente
- **Geocodificación**: Conversión de coordenadas a dirección legible

### Configuración de Google Maps
1. **Obtener API Key**: Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. **Habilitar APIs**: Maps JavaScript API y Places API
3. **Configurar Restricciones**: Para desarrollo y producción
4. **Reemplazar Clave**: En `templates/clima/index.html`

📋 **Guía Completa**: Ver `GOOGLE_MAPS_SETUP.md` para instrucciones detalladas

## 🔧 API Endpoints

### Obtener Pronóstico (JSON)
```
GET /api/pronostico/{id}/
```

**Respuesta:**
```json
{
    "id": 1,
    "fecha": "2024-01-15T10:30:00Z",
    "temperatura": 25.5,
    "humedad": 65.0,
    "presion": 1013.25,
    "velocidad_viento": 15.0,
    "calculos": {
        "indice_calor": 27.3,
        "sensacion_termica": 24.1,
        "punto_rocio": 18.7,
        "presion_ajustada": 1013.25
    },
    "pronostico": {
        "condicion": "Despejado",
        "descripcion": "Cielo despejado con buena visibilidad",
        "probabilidad_lluvia": 0,
        "recomendaciones": []
    },
    "estacion": "Verano"
}
```

## 🎨 Características de la Interfaz

- **Diseño Responsive**: Adaptable a dispositivos móviles y desktop
- **Tema Moderno**: Gradientes y efectos visuales atractivos
- **Iconografía**: Iconos Font Awesome para mejor UX
- **Navegación Intuitiva**: Menú de navegación claro y accesible
- **Feedback Visual**: Alertas y notificaciones para el usuario

## 📈 Métricas Calculadas

### Índice de Calor
- **Fórmula**: Combinación de temperatura y humedad
- **Uso**: Determinar sensación térmica real

### Sensación Térmica
- **Fórmula**: Temperatura + velocidad del viento
- **Uso**: Temperatura percibida por el cuerpo humano

### Punto de Rocío
- **Fórmula**: Fórmula de Magnus
- **Uso**: Predicción de formación de rocío

### Presión Ajustada
- **Fórmula**: Fórmula barométrica
- **Uso**: Comparación con estándares meteorológicos

## 🔍 Análisis del Pronóstico

El sistema analiza múltiples parámetros para determinar:

- **Condición del Tiempo**: Despejado, nublado, lluvioso
- **Probabilidad de Lluvia**: Basada en humedad y nubosidad
- **Recomendaciones**: Consejos según las condiciones
- **Estación del Año**: Determinada por coordenadas y fecha

## 🚀 Despliegue en Producción

### Configuración de Producción
1. Cambiar `DEBUG = False` en settings.py
2. Configurar `ALLOWED_HOSTS` con el dominio
3. Usar base de datos PostgreSQL o MySQL
4. Configurar archivos estáticos
5. Usar servidor web (Nginx + Gunicorn)

### Variables de Entorno
```bash
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Crear un issue en GitHub
- Contactar al desarrollador

---

**Desarrollado con ❤️ usando Django y Python**
