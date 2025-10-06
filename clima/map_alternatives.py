"""
Configuración de alternativas a Google Maps
"""

# Configuración de OpenStreetMap (Recomendado - Gratuito)
OSM_CONFIG = {
    'enabled': True,
    'tile_url': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'attribution': '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    'max_zoom': 19,
    'search_provider': 'nominatim',  # Búsqueda gratuita
    'geocoding_provider': 'nominatim'  # Geocodificación gratuita
}

# Configuración de Mapbox (Requiere API Key)
MAPBOX_CONFIG = {
    'enabled': False,  # Cambiar a True si tienes API key
    'api_key': 'TU_MAPBOX_API_KEY_AQUI',
    'tile_url': 'https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token={accessToken}',
    'attribution': '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a>',
    'max_zoom': 18
}

# Configuración de HERE Maps (Requiere API Key)
HERE_CONFIG = {
    'enabled': False,  # Cambiar a True si tienes API key
    'api_key': 'TU_HERE_API_KEY_AQUI',
    'app_id': 'TU_HERE_APP_ID_AQUI',
    'tile_url': 'https://1.base.maps.ls.hereapi.com/maptile/2.1/maptile/newest/normal.day/{z}/{x}/{y}/256/png8?apikey={apiKey}',
    'attribution': '© <a href="https://developer.here.com">HERE</a>',
    'max_zoom': 18
}

# Configuración de CartoDB (Gratuito con límites)
CARTODB_CONFIG = {
    'enabled': False,
    'tile_url': 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
    'attribution': '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> © <a href="https://carto.com/attributions">CARTO</a>',
    'max_zoom': 19
}

# Configuración por defecto
DEFAULT_MAP_CONFIG = OSM_CONFIG

# Ubicación por defecto (Madrid, España)
DEFAULT_LOCATION = {
    'lat': 40.4168,
    'lng': -3.7038,
    'zoom': 10
}

# Estilos de mapa disponibles
MAP_STYLES = {
    'osm': {
        'name': 'OpenStreetMap',
        'tile_url': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'attribution': '© OpenStreetMap contributors'
    },
    'cartodb_light': {
        'name': 'CartoDB Light',
        'tile_url': 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        'attribution': '© OpenStreetMap © CARTO'
    },
    'cartodb_dark': {
        'name': 'CartoDB Dark',
        'tile_url': 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        'attribution': '© OpenStreetMap © CARTO'
    }
}
