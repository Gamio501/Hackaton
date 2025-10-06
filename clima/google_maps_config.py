"""
Configuración para Google Maps API
"""

# Configuración de Google Maps API
GOOGLE_MAPS_API_KEY = "TU_API_KEY_AQUI"  # Reemplaza con tu API key real

# Configuración por defecto del mapa
DEFAULT_MAP_CENTER = {
    'lat': 40.4168,  # Madrid, España
    'lng': -3.7038
}

DEFAULT_MAP_ZOOM = 10

# Estilos personalizados para el mapa
MAP_STYLES = [
    {
        "featureType": "poi",
        "elementType": "labels",
        "stylers": [{"visibility": "off"}]
    },
    {
        "featureType": "transit",
        "elementType": "labels",
        "stylers": [{"visibility": "off"}]
    }
]

# Configuración de restricciones de API (opcional)
API_RESTRICTIONS = {
    'allowed_referrers': [
        'localhost',
        '127.0.0.1',
        'tu-dominio.com'  # Reemplaza con tu dominio de producción
    ],
    'allowed_ips': [
        '127.0.0.1',
        '::1'
    ]
}
