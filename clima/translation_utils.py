"""
Sistema de traducción estático simple
Sin dependencias externas, solo diccionarios de traducción
"""

# Diccionario de traducciones estáticas
TRANSLATIONS = {
    'es': {
        # Títulos y encabezados
        'Sistema de Pronóstico Climático': 'Sistema de Pronóstico Climático',
        'Pronóstico Climático Inteligente': 'Pronóstico Climático Inteligente',
        'Pronóstico del Clima': 'Pronóstico del Clima',
        'Weather Forecast': 'Pronóstico del Clima',
        
        # Formulario
        'Temperatura': 'Temperatura',
        'Humedad Relativa': 'Humedad Relativa',
        'Presión Atmosférica': 'Presión Atmosférica',
        'Velocidad del Viento': 'Velocidad del Viento',
        'Altura sobre el Nivel del Mar': 'Altura sobre el Nivel del Mar',
        'Nubosidad': 'Nubosidad',
        'Latitud': 'Latitud',
        'Longitud': 'Longitud',
        'Buscar Ubicación': 'Buscar Ubicación',
        'Calcular Pronóstico': 'Calcular Pronóstico',
        'Registros Recientes': 'Registros Recientes',
        'Historial': 'Historial',
        'Dashboard': 'Dashboard',
        'Pronóstico': 'Pronóstico',
        
        # Botones y acciones
        'Buscar': 'Buscar',
        'Limpiar': 'Limpiar',
        'Ver Pronóstico': 'Ver Pronóstico',
        'Volver': 'Volver',
        'Guardar': 'Guardar',
        'Cancelar': 'Cancelar',
        
        # Mensajes
        'Pronóstico calculado exitosamente': 'Pronóstico calculado exitosamente',
        'Error al calcular el pronóstico': 'Error al calcular el pronóstico',
        'No se encontraron datos': 'No se encontraron datos',
        'Ubicación no encontrada': 'Ubicación no encontrada',
        
        # Navegación
        'Inicio': 'Inicio',
        'Mapa OSM': 'Mapa OSM',
        'Mapa NASA': 'Mapa NASA',
        'Historial': 'Historial',
        
        # Unidades
        '°C': '°C',
        '%': '%',
        'hPa': 'hPa',
        'km/h': 'km/h',
        'm': 'm',
        
        # Descripciones
        'Ingrese los datos meteorológicos para calcular el pronóstico': 'Ingrese los datos meteorológicos para calcular el pronóstico',
        'Seleccione una ubicación en el mapa': 'Seleccione una ubicación en el mapa',
        'Datos de la NASA': 'Datos de la NASA',
        'Información': 'Información',
        'Parámetros de Polvo Atmosférico y Aerosoles': 'Parámetros de Polvo Atmosférico y Aerosoles',
        'Densidad de Polvo': 'Densidad de Polvo',
        'Diámetro Medio': 'Diámetro Medio',
        'Desviación del Diámetro': 'Desviación del Diámetro',
        'Profundidad Óptica de Aerosoles': 'Profundidad Óptica de Aerosoles',
        'Visibilidad': 'Visibilidad',
        'Altura de la Capa de Mezcla': 'Altura de la Capa de Mezcla',
        'Calcular Parámetros de Aerosoles': 'Calcular Parámetros de Aerosoles',
        '¡Nuevo!': '¡Nuevo!',
        'Haga clic en el mapa para llenar automáticamente: Latitud, Longitud, Altitud y Nubosidad. Otros campos se completan manualmente.': 'Haga clic en el mapa para llenar automáticamente: Latitud, Longitud, Altitud y Nubosidad. Otros campos se completan manualmente.',
        'Los parámetros de aerosoles se pueden calcular automáticamente usando el botón "Calcular Aerosoles" o ingresar manualmente.': 'Los parámetros de aerosoles se pueden calcular automáticamente usando el botón "Calcular Aerosoles" o ingresar manualmente.',
        'Instrucciones:': 'Instrucciones:',
        'Autocompletar:': 'Autocompletar:',
        'Escriba el nombre de un país, ciudad o lugar': 'Escriba el nombre de un país, ciudad o lugar',
        'Selección:': 'Selección:',
        'Haga clic en una sugerencia o use las flechas del teclado': 'Haga clic en una sugerencia o use las flechas del teclado',
        'Mapa:': 'Mapa:',
        'Haga clic en el mapa para seleccionar la ubicación exacta': 'Haga clic en el mapa para seleccionar la ubicación exacta',
        'Llenado automático:': 'Llenado automático:',
        'Llenado automático: Latitud, Longitud, Altitud y Nubosidad': 'Llenado automático: Latitud, Longitud, Altitud y Nubosidad',
        'Manual:': 'Manual:',
        'Complete temperatura, humedad, presión y viento': 'Complete temperatura, humedad, presión y viento',
        '¡No se requiere clave API!': '¡No se requiere clave API!',
        'Completamente gratuito': 'Completamente gratuito',
        'Campos llenados automáticamente:': 'Campos llenados automáticamente:',
        'Otros campos (temperatura, humedad, presión, viento) deben completarse manualmente.': 'Otros campos (temperatura, humedad, presión, viento) deben completarse manualmente.',
        'Todos los parámetros de polvo atmosférico y aerosoles han sido calculados automáticamente.': 'Todos los parámetros de polvo atmosférico y aerosoles han sido calculados automáticamente.',
        'Nota': 'Nota',
        'Buscar ubicación en el mapa...': 'Buscar ubicación en el mapa...',
        'Busca una ubicación o haz clic en el mapa para seleccionar': 'Busca una ubicación o haz clic en el mapa para seleccionar',
        'Ej: 25.5': 'Ej: 25.5',
        'Ej: 65.0': 'Ej: 65.0',
        'Ej: 1013.25': 'Ej: 1013.25',
        'Ej: 15.0': 'Ej: 15.0',
        'Ej: 100.0': 'Ej: 100.0',
        'Ej: 30.0': 'Ej: 30.0',
        'Se llena automáticamente o ingresa manualmente': 'Se llena automáticamente o ingresa manualmente',
        'Se llena automáticamente o puedes editarlo manualmente': 'Se llena automáticamente o puedes editarlo manualmente',
        'Ej: 15.5': 'Ej: 15.5',
        'Ej: 12.3': 'Ej: 12.3',
        'Ej: 25.7': 'Ej: 25.7',
        'Ej: 2.1': 'Ej: 2.1',
        'Ej: 0.8': 'Ej: 0.8',
        'Ej: 0.15': 'Ej: 0.15',
        'Ej: 10.5': 'Ej: 10.5',
        'Ej: 1200.0': 'Ej: 1200.0',
        'Densidad de partículas de polvo en microgramos por metro cúbico': 'Densidad de partículas de polvo en microgramos por metro cúbico',
        'Concentración de partículas menores a 2.5 micrómetros': 'Concentración de partículas menores a 2.5 micrómetros',
        'Concentración de partículas menores a 10 micrómetros': 'Concentración de partículas menores a 10 micrómetros',
        'Diámetro promedio de las partículas en micrómetros': 'Diámetro promedio de las partículas en micrómetros',
        'Desviación estándar del diámetro de partículas': 'Desviación estándar del diámetro de partículas',
        'Profundidad óptica de aerosoles (adimensional)': 'Profundidad óptica de aerosoles (adimensional)',
        'Visibilidad atmosférica en kilómetros': 'Visibilidad atmosférica en kilómetros',
        'Altura de la capa de mezcla atmosférica en metros': 'Altura de la capa de mezcla atmosférica en metros',
        'Registros de Pronóstico Climático': 'Registros de Pronóstico Climático',
        'Fecha': 'Fecha',
        'Acciones': 'Acciones',
        'No hay registros disponibles': 'No hay registros disponibles',
        'Anterior': 'Anterior',
        'Siguiente': 'Siguiente',
        'Estadísticas del Sistema de Pronóstico Climático': 'Estadísticas del Sistema de Pronóstico Climático',
        'Total de Registros': 'Total de Registros',
        'Temperatura Promedio': 'Temperatura Promedio',
        'Humedad Promedio': 'Humedad Promedio',
        'Presión Promedio': 'Presión Promedio',
        'Viento Promedio': 'Viento Promedio',
        'Último Pronóstico': 'Último Pronóstico',
        'No hay datos disponibles': 'No hay datos disponibles',
        'Pronóstico Detallado': 'Pronóstico Detallado',
        'Análisis Meteorológico Completo': 'Análisis Meteorológico Completo',
        'Índice de Calor': 'Índice de Calor',
        'Sensación Térmica': 'Sensación Térmica',
        'Punto de Rocío': 'Punto de Rocío',
        'Presión Ajustada': 'Presión Ajustada',
        'Estación': 'Estación',
               'Ver Dashboard': 'Ver Dashboard',
               'Registro no encontrado': 'Registro no encontrado',
               'Pronóstico guardado exitosamente': 'Pronóstico guardado exitosamente',
               'Parcialmente nublado': 'Parcialmente nublado',
               'Algunas nubes dispersas': 'Algunas nubes dispersas',
               'Condición': 'Condición',
               'Ubicación': 'Ubicación',
               'Dashboard': 'Dashboard',
        'Ingrese la temperatura en grados Celsius': 'Ingrese la temperatura en grados Celsius',
        'Ingrese la humedad relativa (0-100%)': 'Ingrese la humedad relativa (0-100%)',
        'Ingrese la presión atmosférica en hectopascales': 'Ingrese la presión atmosférica en hectopascales',
        'Ingrese la velocidad del viento en km/h': 'Ingrese la velocidad del viento en km/h',
        'Ingrese la altura sobre el nivel del mar en metros': 'Ingrese la altura sobre el nivel del mar en metros',
        'Ingrese el porcentaje de nubosidad (0-100%)': 'Ingrese el porcentaje de nubosidad (0-100%)',
        
        # Módulo de pronóstico
        'forecast_title': 'Pronóstico del Clima',
        'main_data': 'Datos Principales',
        'location': 'Ubicación',
        'meteorological_calculations': 'Cálculos Meteorológicos',
        'forecast_analysis': 'Análisis del Pronóstico',
        'data_interpretation': 'Interpretación de los Datos',
        'heat_index': 'Índice de Calor',
        'thermal_sensation': 'Sensación Térmica',
        'dew_point': 'Punto de Rocío',
        'adjusted_pressure': 'Presión Ajustada',
        'rain_probability': 'Probabilidad de Lluvia',
        'cloudiness': 'Nubosidad',
        'recommendations': 'Recomendaciones',
        'new_forecast': 'Nuevo Pronóstico',
        'view_history': 'Ver Historial',
        'dashboard': 'Dashboard',
        'latitude': 'Latitud',
        'longitude': 'Longitud',
        'altitude': 'Altura',
        'season': 'Estación',
        'heat_index_description': 'Mide qué tan caliente se siente realmente cuando se combinan la temperatura y la humedad.',
        'thermal_sensation_description': 'Temperatura que siente el cuerpo humano cuando se combinan la temperatura del aire y la velocidad del viento.',
        'dew_point_description': 'Temperatura a la cual el vapor de agua en el aire se condensa en agua líquida.',
        'view_on_map': 'Ver en Mapa',
        'location_details': 'Detalles de Ubicación',
        'Nombre del Lugar': 'Nombre del Lugar',
        'Nombre de la ciudad o lugar donde se realizó el cálculo': 'Nombre de la ciudad o lugar donde se realizó el cálculo',
        'Ej: Lima, Perú': 'Ej: Lima, Perú',
        'place_name': 'Nombre del Lugar',
    },
    
    'en': {
        # Títulos y encabezados
        'Sistema de Pronóstico Climático': 'Weather Forecast System',
        'Pronóstico Climático Inteligente': 'Intelligent Weather Forecast',
        'Pronóstico del Clima': 'Weather Forecast',
        'Weather Forecast': 'Weather Forecast',
        
        # Formulario
        'Temperatura': 'Temperature',
        'Humedad Relativa': 'Relative Humidity',
        'Presión Atmosférica': 'Atmospheric Pressure',
        'Velocidad del Viento': 'Wind Speed',
        'Altura sobre el Nivel del Mar': 'Altitude above Sea Level',
        'Nubosidad': 'Cloudiness',
        'Latitud': 'Latitude',
        'Longitud': 'Longitude',
        'Buscar Ubicación': 'Search Location',
        'Calcular Pronóstico': 'Calculate Forecast',
        'Registros Recientes': 'Recent Records',
        'Historial': 'History',
        'Dashboard': 'Dashboard',
        'Pronóstico': 'Forecast',
        
        # Botones y acciones
        'Buscar': 'Search',
        'Limpiar': 'Clear',
        'Ver Pronóstico': 'View Forecast',
        'Volver': 'Back',
        'Guardar': 'Save',
        'Cancelar': 'Cancel',
        
        # Mensajes
        'Pronóstico calculado exitosamente': 'Forecast calculated successfully',
        'Error al calcular el pronóstico': 'Error calculating forecast',
        'No se encontraron datos': 'No data found',
        'Ubicación no encontrada': 'Location not found',
        
        # Navegación
        'Inicio': 'Home',
        'Mapa OSM': 'OSM Map',
        'Mapa NASA': 'NASA Map',
        'Historial': 'History',
        
        # Unidades
        '°C': '°F',
        '%': '%',
        'hPa': 'hPa',
        'km/h': 'mph',
        'm': 'ft',
        
        # Descripciones
        'Ingrese los datos meteorológicos para calcular el pronóstico': 'Enter meteorological data to calculate forecast',
        'Seleccione una ubicación en el mapa': 'Select a location on the map',
        'Datos de la NASA': 'NASA Data',
        'Información': 'Information',
        'Parámetros de Polvo Atmosférico y Aerosoles': 'Atmospheric Dust and Aerosol Parameters',
        'Densidad de Polvo': 'Dust Density',
        'Diámetro Medio': 'Mean Diameter',
        'Desviación del Diámetro': 'Diameter Deviation',
        'Profundidad Óptica de Aerosoles': 'Aerosol Optical Depth',
        'Visibilidad': 'Visibility',
        'Altura de la Capa de Mezcla': 'Mixing Layer Height',
        'Calcular Parámetros de Aerosoles': 'Calculate Aerosol Parameters',
        '¡Nuevo!': 'New!',
        'Haga clic en el mapa para llenar automáticamente: Latitud, Longitud, Altitud y Nubosidad. Otros campos se completan manualmente.': 'Click on the map to automatically fill: Latitude, Longitude, Altitude and Cloudiness. Other fields are completed manually.',
        'Los parámetros de aerosoles se pueden calcular automáticamente usando el botón "Calcular Aerosoles" o ingresar manualmente.': 'Aerosol parameters can be calculated automatically using the "Calculate Aerosols" button or entered manually.',
        'Instrucciones:': 'Instructions:',
        'Autocompletar:': 'Autocomplete:',
        'Escriba el nombre de un país, ciudad o lugar': 'Type the name of a country, city or place',
        'Selección:': 'Selection:',
        'Haga clic en una sugerencia o use las flechas del teclado': 'Click on a suggestion or use keyboard arrows',
        'Mapa:': 'Map:',
        'Haga clic en el mapa para seleccionar la ubicación exacta': 'Click on the map to select exact location',
        'Llenado automático:': 'Auto-fill:',
        'Llenado automático: Latitud, Longitud, Altitud y Nubosidad': 'Automatically filled: Latitude, Longitude, Altitude and Cloudiness',
        'Manual:': 'Manual:',
        'Complete temperatura, humedad, presión y viento': 'Complete temperature, humidity, pressure and wind',
        '¡No se requiere clave API!': 'No API Key required!',
        'Completamente gratuito': 'Completely free',
        'Campos llenados automáticamente:': 'Automatically filled fields:',
        'Otros campos (temperatura, humedad, presión, viento) deben completarse manualmente.': 'Other fields (temperature, humidity, pressure, wind) must be completed manually.',
        'Todos los parámetros de polvo atmosférico y aerosoles han sido calculados automáticamente.': 'All atmospheric dust and aerosol parameters have been automatically calculated.',
        'Nota': 'Note',
        'Buscar ubicación en el mapa...': 'Search location on the map...',
        'Busca una ubicación o haz clic en el mapa para seleccionar': 'Search for a location or click on the map to select',
        'Ej: 25.5': 'Ex: 25.5',
        'Ej: 65.0': 'Ex: 65.0',
        'Ej: 1013.25': 'Ex: 1013.25',
        'Ej: 15.0': 'Ex: 15.0',
        'Ej: 100.0': 'Ex: 100.0',
        'Ej: 30.0': 'Ex: 30.0',
        'Se llena automáticamente o ingresa manualmente': 'Filled automatically or enter manually',
        'Se llena automáticamente o puedes editarlo manualmente': 'Filled automatically or you can edit it manually',
        'Ej: 15.5': 'Ex: 15.5',
        'Ej: 12.3': 'Ex: 12.3',
        'Ej: 25.7': 'Ex: 25.7',
        'Ej: 2.1': 'Ex: 2.1',
        'Ej: 0.8': 'Ex: 0.8',
        'Ej: 0.15': 'Ex: 0.15',
        'Ej: 10.5': 'Ex: 10.5',
        'Ej: 1200.0': 'Ex: 1200.0',
        'Densidad de partículas de polvo en microgramos por metro cúbico': 'Dust particle density in micrograms per cubic meter',
        'Concentración de partículas menores a 2.5 micrómetros': 'Concentration of particles smaller than 2.5 micrometers',
        'Concentración de partículas menores a 10 micrómetros': 'Concentration of particles smaller than 10 micrometers',
        'Diámetro promedio de las partículas en micrómetros': 'Average particle diameter in micrometers',
        'Desviación estándar del diámetro de partículas': 'Standard deviation of particle diameter',
        'Profundidad óptica de aerosoles (adimensional)': 'Aerosol optical depth (dimensionless)',
        'Visibilidad atmosférica en kilómetros': 'Atmospheric visibility in kilometers',
        'Altura de la capa de mezcla atmosférica en metros': 'Atmospheric mixing layer height in meters',
        'Registros de Pronóstico Climático': 'Weather Forecast Records',
        'Fecha': 'Date',
        'Acciones': 'Actions',
        'No hay registros disponibles': 'No records available',
        'Anterior': 'Previous',
        'Siguiente': 'Next',
        'Estadísticas del Sistema de Pronóstico Climático': 'Weather Forecast System Statistics',
        'Total de Registros': 'Total Records',
        'Temperatura Promedio': 'Average Temperature',
        'Humedad Promedio': 'Average Humidity',
        'Presión Promedio': 'Average Pressure',
        'Viento Promedio': 'Average Wind',
        'Último Pronóstico': 'Last Forecast',
        'No hay datos disponibles': 'No data available',
        'Pronóstico Detallado': 'Detailed Forecast',
        'Análisis Meteorológico Completo': 'Complete Meteorological Analysis',
        'Índice de Calor': 'Heat Index',
        'Sensación Térmica': 'Thermal Sensation',
        'Punto de Rocío': 'Dew Point',
        'Presión Ajustada': 'Adjusted Pressure',
        'Estación': 'Season',
               'Ver Dashboard': 'View Dashboard',
               'Registro no encontrado': 'Record not found',
               'Pronóstico guardado exitosamente': 'Forecast saved successfully',
               'Parcialmente nublado': 'Partly cloudy',
               'Algunas nubes dispersas': 'Some scattered clouds',
               'Condición': 'Condition',
               'Ubicación': 'Location',
               'Dashboard': 'Dashboard',
        'Ingrese la temperatura en grados Celsius': 'Enter the temperature in Celsius degrees',
        'Ingrese la humedad relativa (0-100%)': 'Enter the relative humidity (0-100%)',
        'Ingrese la presión atmosférica en hectopascales': 'Enter the atmospheric pressure in hectopascals',
        'Ingrese la velocidad del viento en km/h': 'Enter the wind speed in km/h',
        'Ingrese la altura sobre el nivel del mar en metros': 'Enter the height above sea level in meters',
        'Ingrese el porcentaje de nubosidad (0-100%)': 'Enter the cloudiness percentage (0-100%)',
        
        # Módulo de pronóstico
        'forecast_title': 'Weather Forecast',
        'main_data': 'Main Data',
        'location': 'Location',
        'meteorological_calculations': 'Meteorological Calculations',
        'forecast_analysis': 'Forecast Analysis',
        'data_interpretation': 'Data Interpretation',
        'heat_index': 'Heat Index',
        'thermal_sensation': 'Thermal Sensation',
        'dew_point': 'Dew Point',
        'adjusted_pressure': 'Adjusted Pressure',
        'rain_probability': 'Rain Probability',
        'cloudiness': 'Cloudiness',
        'recommendations': 'Recommendations',
        'new_forecast': 'New Forecast',
        'view_history': 'View History',
        'dashboard': 'Dashboard',
        'latitude': 'Latitude',
        'longitude': 'Longitude',
        'altitude': 'Altitude',
        'season': 'Season',
        'heat_index_description': 'Measures how hot it really feels when temperature and humidity are combined.',
        'thermal_sensation_description': 'Temperature that the human body feels when air temperature and wind speed are combined.',
        'dew_point_description': 'Temperature at which water vapor in the air condenses into liquid water.',
        'view_on_map': 'View on Map',
        'location_details': 'Location Details',
        'Nombre del Lugar': 'Place Name',
        'Nombre de la ciudad o lugar donde se realizó el cálculo': 'Name of the city or place where the calculation was performed',
        'Ej: Lima, Perú': 'Ex: Lima, Peru',
        'place_name': 'Place Name',
    }
}

def get_text(text, language='en'):
    """
    Obtener texto traducido
    """
    if language in TRANSLATIONS and text in TRANSLATIONS[language]:
        return TRANSLATIONS[language][text]
    return text

def get_language_from_request(request):
    """
    Obtener idioma de la request (URL parameter o cookie)
    """
    # Primero verificar parámetro de URL
    lang = request.GET.get('lang', '')
    if lang in ['es', 'en']:
        return lang
    
    # Luego verificar cookie
    lang = request.COOKIES.get('language', '')
    if lang in ['es', 'en']:
        return lang
    
    # Por defecto inglés
    return 'en'

def set_language_cookie(response, language):
    """
    Establecer cookie de idioma
    """
    response.set_cookie('language', language, max_age=60*60*24*7)  # 7 días
    return response

def convert_temperature(celsius, to_fahrenheit=True):
    """
    Convertir temperatura entre Celsius y Fahrenheit
    """
    if to_fahrenheit:
        return round((celsius * 9/5) + 32, 1)
    else:
        return round((celsius - 32) * 5/9, 1)

def convert_wind_speed(kmh, to_mph=True):
    """
    Convertir velocidad del viento entre km/h y mph
    """
    if to_mph:
        return round(kmh * 0.621371, 1)
    else:
        return round(kmh / 0.621371, 1)

def convert_distance(meters, to_feet=True):
    """
    Convertir distancia entre metros y pies
    """
    if to_feet:
        return round(meters * 3.28084, 1)
    else:
        return round(meters / 3.28084, 1)

def convert_visibility(km, to_miles=True):
    """
    Convertir visibilidad entre km y millas
    """
    if to_miles:
        return round(km * 0.621371, 1)
    else:
        return round(km / 0.621371, 1)

def convert_pressure_to_display(pressure_in_hpa, to_inhg=True):
    """
    Convertir presión entre hPa e inHg
    """
    if to_inhg:
        # Convertir hPa a inHg: 1 hPa = 0.029529983071445 inHg
        return round(pressure_in_hpa * 0.029529983071445, 3)
    else:
        return round(pressure_in_hpa, 2)
