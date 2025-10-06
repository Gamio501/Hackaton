# Configuración para integración con NASA Worldview/GIBS
# Global Imagery Browse Services (GIBS) de la NASA

# Configuración de capas de datos satelitales de la NASA
NASA_LAYERS = {
    # Imágenes satelitales básicas
    'MODIS_Terra_CorrectedReflectance_TrueColor': {
        'name': 'Imagen Satelital (Color Real)',
        'description': 'Imagen satelital en color real de la Tierra',
        'category': 'visual',
        'time_enabled': True,
        'resolution': '250m'
    },
    'MODIS_Aqua_CorrectedReflectance_TrueColor': {
        'name': 'Imagen Satelital Aqua (Color Real)',
        'description': 'Imagen satelital en color real del satélite Aqua',
        'category': 'visual',
        'time_enabled': True,
        'resolution': '250m'
    },
    
    # Datos de temperatura
    'MODIS_Terra_Land_Surface_Temperature_Day': {
        'name': 'Temperatura Superficie (Día)',
        'description': 'Temperatura de la superficie terrestre durante el día',
        'category': 'temperature',
        'time_enabled': True,
        'resolution': '1km',
        'unit': '°C'
    },
    'MODIS_Terra_Land_Surface_Temperature_Night': {
        'name': 'Temperatura Superficie (Noche)',
        'description': 'Temperatura de la superficie terrestre durante la noche',
        'category': 'temperature',
        'time_enabled': True,
        'resolution': '1km',
        'unit': '°C'
    },
    
    # Datos de nubes
    'MODIS_Terra_Cloud_Fraction': {
        'name': 'Fracción Nubosa',
        'description': 'Porcentaje de cobertura nubosa',
        'category': 'clouds',
        'time_enabled': True,
        'resolution': '1km',
        'unit': '%'
    },
    'MODIS_Terra_Cloud_Optical_Thickness': {
        'name': 'Espesor Óptico de Nubes',
        'description': 'Espesor óptico de las nubes',
        'category': 'clouds',
        'time_enabled': True,
        'resolution': '1km'
    },
    'MODIS_Terra_Cloud_Top_Temperature': {
        'name': 'Temperatura de Nubes',
        'description': 'Temperatura en la parte superior de las nubes',
        'category': 'clouds',
        'time_enabled': True,
        'resolution': '1km',
        'unit': '°C'
    },
    'MODIS_Terra_Cloud_Top_Height': {
        'name': 'Altura de Nubes',
        'description': 'Altura de la parte superior de las nubes',
        'category': 'clouds',
        'time_enabled': True,
        'resolution': '1km',
        'unit': 'km'
    },
    
    # Datos atmosféricos
    'MODIS_Terra_Aerosol_Optical_Depth': {
        'name': 'Profundidad Óptica de Aerosoles',
        'description': 'Medida de la cantidad de aerosoles en la atmósfera',
        'category': 'atmosphere',
        'time_enabled': True,
        'resolution': '10km'
    },
    'MODIS_Terra_Water_Vapor': {
        'name': 'Vapor de Agua',
        'description': 'Contenido de vapor de agua en la atmósfera',
        'category': 'atmosphere',
        'time_enabled': True,
        'resolution': '1km',
        'unit': 'g/cm²'
    },
    
    # Datos de precipitación
    'GPM_3IMERGHH': {
        'name': 'Precipitación GPM',
        'description': 'Datos de precipitación del Global Precipitation Measurement',
        'category': 'precipitation',
        'time_enabled': True,
        'resolution': '0.1°'
    },
    
    # Datos de viento
    'MODIS_Terra_Wind_Speed': {
        'name': 'Velocidad del Viento',
        'description': 'Velocidad del viento en superficie',
        'category': 'wind',
        'time_enabled': True,
        'resolution': '1km',
        'unit': 'm/s'
    }
}

# Configuración de categorías para organización
LAYER_CATEGORIES = {
    'visual': {
        'name': 'Imágenes Visuales',
        'icon': 'fas fa-eye',
        'color': '#4CAF50'
    },
    'temperature': {
        'name': 'Temperatura',
        'icon': 'fas fa-thermometer-half',
        'color': '#FF5722'
    },
    'clouds': {
        'name': 'Nubes',
        'icon': 'fas fa-cloud',
        'color': '#2196F3'
    },
    'atmosphere': {
        'name': 'Atmósfera',
        'icon': 'fas fa-wind',
        'color': '#9C27B0'
    },
    'precipitation': {
        'name': 'Precipitación',
        'icon': 'fas fa-cloud-rain',
        'color': '#00BCD4'
    },
    'wind': {
        'name': 'Viento',
        'icon': 'fas fa-fan',
        'color': '#FF9800'
    }
}

# URLs base para los servicios GIBS
GIBS_BASE_URLS = {
    'wmts': 'https://gibs.earthdata.nasa.gov/wmts/epsg4326/best',
    'wms': 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best',
    'tile': 'https://gibs.earthdata.nasa.gov/wmts/epsg4326/best'
}

# Configuración de proyecciones soportadas
SUPPORTED_PROJECTIONS = {
    'EPSG:4326': 'WGS84 (Lat/Lon)',
    'EPSG:3857': 'Web Mercator'
}

# Configuración de resoluciones disponibles
RESOLUTIONS = {
    '250m': '250 metros',
    '1km': '1 kilómetro',
    '10km': '10 kilómetros',
    '0.1°': '0.1 grados'
}

# Configuración de tiempo (días hacia atrás desde hoy)
TIME_RANGE_DAYS = 7

# Configuración de colores para las capas
LAYER_COLORS = {
    'temperature': {
        'min': '#000080',  # Azul oscuro
        'max': '#FF0000'   # Rojo
    },
    'clouds': {
        'min': '#FFFFFF',  # Blanco
        'max': '#000000'   # Negro
    },
    'precipitation': {
        'min': '#FFFFFF',  # Blanco
        'max': '#0000FF'   # Azul
    }
}

# Función para obtener URL de capa
def get_layer_url(layer_id, time=None, resolution='250m'):
    """
    Genera la URL para una capa específica de NASA GIBS
    
    Args:
        layer_id (str): ID de la capa
        time (str): Fecha en formato YYYY-MM-DD (opcional)
        resolution (str): Resolución de la capa
    
    Returns:
        str: URL completa para la capa
    """
    if time is None:
        from datetime import datetime
        time = datetime.now().strftime('%Y-%m-%d')
    
    base_url = GIBS_BASE_URLS['wmts']
    layer_config = NASA_LAYERS.get(layer_id, {})
    
    if not layer_config:
        return None
    
    # Construir URL según el tipo de capa
    if layer_config.get('time_enabled', False):
        url_template = f"{base_url}/{layer_id}/default/{{Time}}/{{TileMatrixSet}}/{{z}}/{{y}}/{{x}}.png"
    else:
        url_template = f"{base_url}/{layer_id}/default/{{TileMatrixSet}}/{{z}}/{{y}}/{{x}}.png"
    
    return url_template

# Función para obtener capas por categoría
def get_layers_by_category(category):
    """
    Obtiene todas las capas de una categoría específica
    
    Args:
        category (str): Categoría de las capas
    
    Returns:
        dict: Diccionario con las capas de la categoría
    """
    return {
        layer_id: config 
        for layer_id, config in NASA_LAYERS.items() 
        if config.get('category') == category
    }

# Función para obtener información de una capa
def get_layer_info(layer_id):
    """
    Obtiene información detallada de una capa específica
    
    Args:
        layer_id (str): ID de la capa
    
    Returns:
        dict: Información de la capa o None si no existe
    """
    return NASA_LAYERS.get(layer_id)

# Función para validar si una capa está disponible
def is_layer_available(layer_id):
    """
    Verifica si una capa está disponible
    
    Args:
        layer_id (str): ID de la capa
    
    Returns:
        bool: True si la capa está disponible
    """
    return layer_id in NASA_LAYERS
