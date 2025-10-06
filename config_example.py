# Configuración de ejemplo para Google Maps API
# Copia este archivo como config.py y configura tu API key

# Tu API Key de Google Maps (obtén una en https://console.cloud.google.com/)
GOOGLE_MAPS_API_KEY = "AIzaSyBvOkBwvBwvBwvBwvBwvBwvBwvBwvBwvBw"  # Reemplaza con tu clave real

# Configuración del mapa por defecto
DEFAULT_LOCATION = {
    'lat': 40.4168,  # Madrid, España
    'lng': -3.7038
}

# Zoom inicial del mapa
DEFAULT_ZOOM = 10

# Restricciones de seguridad (opcional)
ALLOWED_DOMAINS = [
    'localhost',
    '127.0.0.1',
    'tu-dominio.com'
]
