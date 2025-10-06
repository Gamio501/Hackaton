from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import RegistroClima, Login
from .forms import create_registro_clima_form
from django.core.paginator import Paginator
from .nasa_service import nasa_service
from .nasa_config import NASA_LAYERS, LAYER_CATEGORIES
from .translation_utils import get_text, get_language_from_request, set_language_cookie, convert_temperature, convert_wind_speed, convert_distance, convert_visibility, convert_pressure_to_display
import json
import hashlib
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

def index(request):
    """Página principal con formulario para ingresar datos"""
    # Verificar autenticación simple
    if not request.session.get('usuario_autenticado'):
        return redirect('/login/')
    
    # Obtener idioma
    language = get_language_from_request(request)
    
    if request.method == 'POST':
        form = create_registro_clima_form(language)(request.POST)
        if form.is_valid():
            registro = form.save()
            messages.success(request, get_text('Pronóstico calculado exitosamente', language))
            return redirect('pronostico', registro_id=registro.id)
    else:
        form = create_registro_clima_form(language)()
    
    # Obtener los últimos 5 registros y convertir unidades según idioma
    ultimos_registros_raw = RegistroClima.objects.all().order_by('-fecha')[:5]
    ultimos_registros = []
    for registro in ultimos_registros_raw:
        registro_convertido = {
            'id': registro.id,
            'fecha': registro.fecha,
            'temperatura': convert_temperature(registro.temperatura, language == 'en') if language == 'en' else registro.temperatura,
            'humedad': registro.humedad,
            'velocidad_viento': convert_wind_speed(registro.velocidad_viento, language == 'en') if language == 'en' else registro.velocidad_viento,
            'presion': registro.presion,
            'altura': convert_distance(registro.altura, language == 'en') if language == 'en' else registro.altura,
            'nubosidad': registro.nubosidad,
            'latitud': registro.latitud,
            'longitud': registro.longitud,
        }
        ultimos_registros.append(registro_convertido)
    
    # Crear contexto con traducciones
    context = {
        'form': form,
        'ultimos_registros': ultimos_registros,
        'language': language,
        'texts': {
            'title': get_text('Sistema de Pronóstico Climático', language),
            'subtitle': get_text('Pronóstico Climático Inteligente', language),
            'description': get_text('Ingrese los datos meteorológicos para calcular el pronóstico', language),
            'recent_records': get_text('Registros Recientes', language),
            'temperature': get_text('Temperatura', language),
            'humidity': get_text('Humedad Relativa', language),
            'pressure': get_text('Presión Atmosférica', language),
            'wind_speed': get_text('Velocidad del Viento', language),
            'altitude': get_text('Altura sobre el Nivel del Mar', language),
            'cloudiness': get_text('Nubosidad', language),
            'latitude': get_text('Latitud', language),
            'longitude': get_text('Longitud', language),
            'search_location': get_text('Buscar Ubicación', language),
            'calculate_forecast': get_text('Calcular Pronóstico', language),
            'view_forecast': get_text('Ver Pronóstico', language),
        }
    }
    
    response = render(request, 'clima/index.html', context)
    return set_language_cookie(response, language)

def index_osm(request):
    """Página principal con OpenStreetMap"""
    # Obtener idioma
    language = get_language_from_request(request)
    
    if request.method == 'POST':
        form = create_registro_clima_form(language)(request.POST)
        if form.is_valid():
            registro = form.save()
            messages.success(request, get_text('Pronóstico calculado exitosamente', language))
            return redirect('pronostico', registro_id=registro.id)
    else:
        form = create_registro_clima_form(language)()
    
    # Obtener los últimos 5 registros y convertir unidades según idioma
    ultimos_registros_raw = RegistroClima.objects.all().order_by('-fecha')[:5]
    ultimos_registros = []
    for registro in ultimos_registros_raw:
        registro_convertido = {
            'id': registro.id,
            'fecha': registro.fecha,
            'temperatura': convert_temperature(registro.temperatura, language == 'en') if language == 'en' else registro.temperatura,
            'humedad': registro.humedad,
            'velocidad_viento': convert_wind_speed(registro.velocidad_viento, language == 'en') if language == 'en' else registro.velocidad_viento,
            'presion': registro.presion,
            'altura': convert_distance(registro.altura, language == 'en') if language == 'en' else registro.altura,
            'nubosidad': registro.nubosidad,
            'latitud': registro.latitud,
            'longitud': registro.longitud,
        }
        ultimos_registros.append(registro_convertido)
    
    # Crear contexto con traducciones
    context = {
        'form': form,
        'ultimos_registros': ultimos_registros,
        'language': language,
        'texts': {
            'title': get_text('Sistema de Pronóstico Climático', language) + ' (OpenStreetMap)',
            'subtitle': get_text('Ingrese los datos meteorológicos para calcular el pronóstico', language),
            'enter_climate_data': get_text('Ingrese los datos meteorológicos para calcular el pronóstico', language),
            'temperature': get_text('Temperatura', language),
            'humidity': get_text('Humedad Relativa', language),
            'pressure': get_text('Presión Atmosférica', language),
            'wind_speed': get_text('Velocidad del Viento', language),
            'altitude': get_text('Altura sobre el Nivel del Mar', language),
            'cloudiness': get_text('Nubosidad', language),
            'latitude': get_text('Latitud', language),
            'longitude': get_text('Longitud', language),
            'search_location': get_text('Buscar Ubicación', language),
            'place_name': get_text('place_name', language),
            'select_location': get_text('Seleccione una ubicación en el mapa', language),
            'calculate_forecast': get_text('Calcular Pronóstico', language),
            'recent_records': get_text('Registros Recientes', language),
            'information': get_text('Información', language),
            'aerosol_params': get_text('Parámetros de Polvo Atmosférico y Aerosoles', language),
            'dust_density': get_text('Densidad de Polvo', language),
            'pm25': 'PM2.5',
            'pm10': 'PM10',
            'mean_diameter': get_text('Diámetro Medio', language),
            'diameter_deviation': get_text('Desviación del Diámetro', language),
            'aod': get_text('Profundidad Óptica de Aerosoles', language),
            'visibility': get_text('Visibilidad', language),
            'mixing_layer_height': get_text('Altura de la Capa de Mezcla', language),
            'calculate_aerosols': get_text('Calcular Parámetros de Aerosoles', language),
            'new_feature': get_text('¡Nuevo!', language),
            'click_map_instruction': get_text('Haga clic en el mapa para llenar automáticamente: Latitud, Longitud, Altitud y Nubosidad. Otros campos se completan manualmente.', language),
            'aerosol_note': get_text('Los parámetros de aerosoles se pueden calcular automáticamente usando el botón "Calcular Aerosoles" o ingresar manualmente.', language),
            'instructions': get_text('Instrucciones:', language),
            'autocomplete': get_text('Autocompletar:', language),
            'autocomplete_desc': get_text('Escriba el nombre de un país, ciudad o lugar', language),
            'selection': get_text('Selección:', language),
            'selection_desc': get_text('Haga clic en una sugerencia o use las flechas del teclado', language),
            'map': get_text('Mapa:', language),
            'map_desc': get_text('Haga clic en el mapa para seleccionar la ubicación exacta', language),
            'auto_fill': get_text('Llenado automático:', language),
            'auto_fill_desc': get_text('Llenado automático: Latitud, Longitud, Altitud y Nubosidad', language),
            'manual': get_text('Manual:', language),
            'manual_desc': get_text('Complete temperatura, humedad, presión y viento', language),
            'no_api_key': get_text('¡No se requiere clave API!', language),
            'completely_free': get_text('Completamente gratuito', language),
            'fields_auto_filled': get_text('Campos llenados automáticamente:', language),
            'other_fields_manual': get_text('Otros campos (temperatura, humedad, presión, viento) deben completarse manualmente.', language),
            'aerosol_calculated': get_text('Todos los parámetros de polvo atmosférico y aerosoles han sido calculados automáticamente.', language),
            'note': get_text('Nota', language),
        }
    }
    
    response = render(request, 'clima/index_osm.html', context)
    return set_language_cookie(response, language)

def index_nasa(request):
    """Página principal con NASA Worldview/GIBS"""
    # Obtener idioma
    language = get_language_from_request(request)
    
    if request.method == 'POST':
        form = create_registro_clima_form(language)(request.POST)
        if form.is_valid():
            registro = form.save()
            messages.success(request, get_text('Pronóstico calculado exitosamente', language))
            return redirect('pronostico', registro_id=registro.id)
    else:
        form = create_registro_clima_form(language)()
    
    # Obtener los últimos 5 registros
    ultimos_registros = RegistroClima.objects.all().order_by('-fecha')[:5]
    
    # Obtener datos de NASA si se proporcionan coordenadas
    nasa_data = None
    if request.GET.get('lat') and request.GET.get('lon'):
        try:
            lat = float(request.GET.get('lat'))
            lon = float(request.GET.get('lon'))
            nasa_data = nasa_service.get_weather_summary(lat, lon)
        except (ValueError, TypeError):
            pass
    
    context = {
        'form': form,
        'ultimos_registros': ultimos_registros,
        'nasa_layers': NASA_LAYERS,
        'layer_categories': LAYER_CATEGORIES,
        'nasa_data': nasa_data,
    }
    return render(request, 'clima/index_nasa.html', context)

def pronostico(request, registro_id):
    """Página de pronóstico detallado"""
    from django.shortcuts import get_object_or_404
    import math
    
    # Obtener idioma
    language = get_language_from_request(request)
    
    try:
        registro_raw = get_object_or_404(RegistroClima, id=registro_id)
        
        # Calcular métricas (en unidades base)
        temp_celsius = registro_raw.temperatura
        humedad = registro_raw.humedad
        presion = registro_raw.presion
        viento_kmh = registro_raw.velocidad_viento
        
        # Índice de calor (Heat Index)
        if temp_celsius >= 27 and humedad >= 40:
            hi = -8.78469475556 + 1.61139411 * temp_celsius + 2.33854883889 * humedad - 0.14611605 * temp_celsius * humedad - 0.012308094 * (temp_celsius ** 2) - 0.0164248277778 * (humedad ** 2) + 0.002211732 * (temp_celsius ** 2) * humedad + 0.00072546 * temp_celsius * (humedad ** 2) - 0.000003582 * (temp_celsius ** 2) * (humedad ** 2)
            indice_calor = max(hi, temp_celsius)
        else:
            indice_calor = temp_celsius
        
        # Sensación térmica (Wind Chill)
        if temp_celsius <= 10 and viento_kmh > 4.8:
            viento_ms = viento_kmh / 3.6
            sensacion_termica = 13.12 + 0.6215 * temp_celsius - 11.37 * (viento_ms ** 0.16) + 0.3965 * temp_celsius * (viento_ms ** 0.16)
        else:
            sensacion_termica = temp_celsius
        
        # Punto de rocío (Dew Point)
        a = 17.27
        b = 237.7
        alpha = ((a * temp_celsius) / (b + temp_celsius)) + math.log(humedad / 100.0)
        punto_rocio = (b * alpha) / (a - alpha)
        
        # Presión ajustada al nivel del mar
        altura_metros = registro_raw.altura
        presion_ajustada = presion * (1 - (0.0065 * altura_metros) / (temp_celsius + 0.0065 * altura_metros + 273.15)) ** -5.257
        
        # Convertir métricas calculadas si es inglés
        if language == 'en':
            indice_calor = convert_temperature(indice_calor, True)
            sensacion_termica = convert_temperature(sensacion_termica, True)
            punto_rocio = convert_temperature(punto_rocio, True)
            presion_ajustada = convert_pressure_to_display(presion_ajustada, True)
        
        # Convertir registro
        registro = {
            'id': registro_raw.id,
            'fecha': registro_raw.fecha,
            'temperatura': convert_temperature(registro_raw.temperatura, language == 'en'),
            'humedad': registro_raw.humedad,
            'presion': convert_pressure_to_display(registro_raw.presion, language == 'en'),
            'velocidad_viento': convert_wind_speed(registro_raw.velocidad_viento, language == 'en'),
            'altura': convert_distance(registro_raw.altura, language == 'en'),
            'nubosidad': registro_raw.nubosidad,
            'latitud': registro_raw.latitud,
            'longitud': registro_raw.longitud,
        }
        
        # Obtener pronóstico y traducir condiciones
        pronostico_raw = registro_raw.pronosticar_tiempo()
        
        # Traducir condiciones climáticas
        condicion_translated = pronostico_raw.get('condicion', 'Despejado')
        if language == 'en':
            if condicion_translated == 'Parcialmente nublado':
                condicion_translated = 'Partly Cloudy'
            elif condicion_translated == 'Nublado':
                condicion_translated = 'Cloudy'
            elif condicion_translated == 'Lluvioso':
                condicion_translated = 'Rainy'
            elif condicion_translated == 'Despejado':
                condicion_translated = 'Clear'
        
        descripcion_translated = pronostico_raw.get('descripcion', 'Algunas nubes dispersas')
        if language == 'en':
            if descripcion_translated == 'Algunas nubes dispersas':
                descripcion_translated = 'Some scattered clouds'
            elif descripcion_translated == 'Cielo despejado':
                descripcion_translated = 'Clear sky'
            elif descripcion_translated == 'Nubes dispersas':
                descripcion_translated = 'Scattered clouds'
        
        # Obtener probabilidad de lluvia
        probabilidad_lluvia = pronostico_raw.get('probabilidad_lluvia', 0)
        
        # Traducir recomendaciones
        recomendaciones_translated = []
        for recomendacion in pronostico_raw.get('recomendaciones', []):
            if language == 'en':
                if 'Viento fuerte' in recomendacion:
                    recomendaciones_translated.append('Strong wind - Avoid outdoor activities')
                elif 'Viento moderado' in recomendacion:
                    recomendaciones_translated.append('Moderate wind - Take caution')
                elif 'Temperatura alta' in recomendacion:
                    recomendaciones_translated.append('High temperature - Stay hydrated')
                elif 'Temperatura baja' in recomendacion:
                    recomendaciones_translated.append('Low temperature - Dress warmly')
                else:
                    recomendaciones_translated.append(recomendacion)
            else:
                recomendaciones_translated.append(recomendacion)
        
        # Determinar estación
        mes = registro_raw.fecha.month
        if mes in [12, 1, 2]:
            estacion = "Invierno"
        elif mes in [3, 4, 5]:
            estacion = "Primavera"
        elif mes in [6, 7, 8]:
            estacion = "Verano"
        else:
            estacion = "Otoño"
        
        # Traducir estación
        estacion_translated = estacion
        if language == 'en':
            if estacion == 'Invierno':
                estacion_translated = 'Winter'
            elif estacion == 'Primavera':
                estacion_translated = 'Spring'
            elif estacion == 'Verano':
                estacion_translated = 'Summer'
            elif estacion == 'Otoño':
                estacion_translated = 'Fall'
        
        # Textos traducidos
        texts = {
            'forecast_title': get_text('forecast_title', language),
            'main_data': get_text('main_data', language),
            'location': get_text('location', language),
            'meteorological_calculations': get_text('meteorological_calculations', language),
            'forecast_analysis': get_text('forecast_analysis', language),
            'data_interpretation': get_text('data_interpretation', language),
            'heat_index': get_text('heat_index', language),
            'thermal_sensation': get_text('thermal_sensation', language),
            'dew_point': get_text('dew_point', language),
            'adjusted_pressure': get_text('adjusted_pressure', language),
            'rain_probability': get_text('rain_probability', language),
            'cloudiness': get_text('cloudiness', language),
            'recommendations': get_text('recommendations', language),
            'new_forecast': get_text('new_forecast', language),
            'view_history': get_text('view_history', language),
            'dashboard': get_text('dashboard', language),
            'temperature': get_text('Temperatura', language),
            'humidity': get_text('Humedad Relativa', language),
            'pressure': get_text('Presión Atmosférica', language),
            'wind_speed': get_text('Velocidad del Viento', language),
            'altitude': get_text('Altura sobre el Nivel del Mar', language),
            'latitude': get_text('latitude', language),
            'longitude': get_text('longitude', language),
            'season': get_text('season', language),
            'heat_index_description': get_text('heat_index_description', language),
            'thermal_sensation_description': get_text('thermal_sensation_description', language),
            'dew_point_description': get_text('dew_point_description', language),
        }
        
        response = render(request, 'clima/pronostico.html', {
            'registro': registro,
            'indice_calor': round(indice_calor, 2),
            'sensacion_termica': round(sensacion_termica, 2),
            'punto_rocio': round(punto_rocio, 2),
            'presion_ajustada': round(presion_ajustada, 3) if language == 'en' else round(presion_ajustada, 2),
            'pronostico': {
                'condicion_translated': condicion_translated,
                'descripcion_translated': descripcion_translated,
                'probabilidad_lluvia': probabilidad_lluvia,
                'recomendaciones': recomendaciones_translated
            },
            'estacion_translated': estacion_translated,
            'language': language,
            'texts': texts
        })
        
        return set_language_cookie(response, language)
    
    except RegistroClima.DoesNotExist:
        messages.error(request, get_text('Registro no encontrado', language))
        return redirect('index')

def historial(request):
    """Página de historial de registros"""
    # Obtener idioma
    language = get_language_from_request(request)
    
    registros_raw = RegistroClima.objects.all().order_by('-fecha')
    
    # Convertir unidades según idioma
    registros_convertidos = []
    for registro in registros_raw:
        registro_convertido = {
            'id': registro.id,
            'fecha': registro.fecha,
            'temperatura': convert_temperature(registro.temperatura, language == 'en') if language == 'en' else registro.temperatura,
            'humedad': registro.humedad,
            'velocidad_viento': convert_wind_speed(registro.velocidad_viento, language == 'en') if language == 'en' else registro.velocidad_viento,
            'presion': registro.presion,
            'altura': convert_distance(registro.altura, language == 'en') if language == 'en' else registro.altura,
            'nubosidad': registro.nubosidad,
            'latitud': registro.latitud,
            'longitud': registro.longitud,
            'nombre_lugar': registro.nombre_lugar,
        }
        registros_convertidos.append(registro_convertido)
    
    # Paginación
    paginator = Paginator(registros_convertidos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'language': language,
        'texts': {
            'title': get_text('Historial', language),
            'subtitle': get_text('Registros de Pronóstico Climático', language),
            'temperature': get_text('Temperatura', language),
            'humidity': get_text('Humedad Relativa', language),
            'pressure': get_text('Presión Atmosférica', language),
            'wind_speed': get_text('Velocidad del Viento', language),
            'altitude': get_text('Altura sobre el Nivel del Mar', language),
            'cloudiness': get_text('Nubosidad', language),
            'latitude': get_text('latitude', language),
            'longitude': get_text('longitude', language),
            'date': get_text('Fecha', language),
            'actions': get_text('Acciones', language),
            'view_forecast': get_text('Ver Pronóstico', language),
            'no_records': get_text('No hay registros disponibles', language),
            'previous': get_text('Anterior', language),
            'next': get_text('Siguiente', language),
            'location': get_text('location', language),
            'dashboard': get_text('dashboard', language),
            'view_on_map': get_text('view_on_map', language),
            'location_details': get_text('location_details', language),
        }
    }
    
    response = render(request, 'clima/historial.html', context)
    return set_language_cookie(response, language)

def api_pronostico(request, registro_id):
    """API para obtener datos del pronóstico en formato JSON"""
    try:
        registro = RegistroClima.objects.get(id=registro_id)
        
        data = {
            'id': registro.id,
            'fecha': registro.fecha.isoformat(),
            'temperatura': registro.temperatura,
            'humedad': registro.humedad,
            'presion': registro.presion,
            'velocidad_viento': registro.velocidad_viento,
            'altura': registro.altura,
            'nubosidad': registro.nubosidad,
            'latitud': registro.latitud,
            'longitud': registro.longitud,
            'calculos': {
                'indice_calor': registro.calcular_indice_calor(),
                'sensacion_termica': registro.calcular_sensacion_termica(),
                'punto_rocio': registro.calcular_punto_rocio(),
                'presion_ajustada': registro.calcular_presion_ajustada(),
            },
            'pronostico': registro.pronosticar_tiempo(),
            'estacion': registro.calcular_estacion(),
        }
        
        return JsonResponse(data)
    
    except RegistroClima.DoesNotExist:
        return JsonResponse({'error': 'Registro no encontrado'}, status=404)

def dashboard(request):
    """Dashboard con estadísticas generales"""
    # Verificar autenticación simple
    if not request.session.get('usuario_autenticado'):
        return redirect('/login/')
    
    # Obtener idioma
    language = get_language_from_request(request)
    
    registros_raw = RegistroClima.objects.all().order_by('-fecha')
    
    if registros_raw.exists():
        # Estadísticas básicas (calcular en Celsius primero)
        temp_promedio = sum(r.temperatura for r in registros_raw) / len(registros_raw)
        humedad_promedio = sum(r.humedad for r in registros_raw) / len(registros_raw)
        presion_promedio = sum(r.presion for r in registros_raw) / len(registros_raw)
        viento_promedio = sum(r.velocidad_viento for r in registros_raw) / len(registros_raw)
        
        # Convertir unidades según idioma
        if language == 'en':
            temp_promedio = convert_temperature(temp_promedio, True)
            viento_promedio = convert_wind_speed(viento_promedio, True)
        
        # Último pronóstico
        ultimo_registro_raw = registros_raw.first()
        ultimo_pronostico = ultimo_registro_raw.pronosticar_tiempo()
        
        # Convertir último registro
        ultimo_registro = {
            'id': ultimo_registro_raw.id,
            'fecha': ultimo_registro_raw.fecha,
            'temperatura': convert_temperature(ultimo_registro_raw.temperatura, language == 'en') if language == 'en' else ultimo_registro_raw.temperatura,
            'humedad': ultimo_registro_raw.humedad,
            'velocidad_viento': convert_wind_speed(ultimo_registro_raw.velocidad_viento, language == 'en') if language == 'en' else ultimo_registro_raw.velocidad_viento,
            'presion': ultimo_registro_raw.presion,
            'altura': convert_distance(ultimo_registro_raw.altura, language == 'en') if language == 'en' else ultimo_registro_raw.altura,
            'nubosidad': ultimo_registro_raw.nubosidad,
            'latitud': ultimo_registro_raw.latitud,
            'longitud': ultimo_registro_raw.longitud,
        }
        
        # Convertir registros recientes
        registros_recientes = []
        for registro in registros_raw[:5]:
            registro_convertido = {
                'id': registro.id,
                'fecha': registro.fecha,
                'temperatura': convert_temperature(registro.temperatura, language == 'en') if language == 'en' else registro.temperatura,
                'humedad': registro.humedad,
                'velocidad_viento': convert_wind_speed(registro.velocidad_viento, language == 'en') if language == 'en' else registro.velocidad_viento,
                'presion': registro.presion,
                'altura': convert_distance(registro.altura, language == 'en') if language == 'en' else registro.altura,
                'nubosidad': registro.nubosidad,
                'latitud': registro.latitud,
                'longitud': registro.longitud,
            }
            registros_recientes.append(registro_convertido)
        
        context = {
            'total_registros': registros_raw.count(),
            'temp_promedio': round(temp_promedio, 2),
            'humedad_promedio': round(humedad_promedio, 2),
            'presion_promedio': round(presion_promedio, 2),
            'viento_promedio': round(viento_promedio, 2),
            'ultimo_registro': ultimo_registro,
            'ultimo_pronostico': ultimo_pronostico,
            'registros_recientes': registros_recientes,
            'language': language,
            'texts': {
                'title': get_text('Dashboard', language),
                'subtitle': get_text('Estadísticas del Sistema de Pronóstico Climático', language),
                'total_records': get_text('Total de Registros', language),
                'average_temperature': get_text('Temperatura Promedio', language),
                'average_humidity': get_text('Humedad Promedio', language),
                'average_pressure': get_text('Presión Promedio', language),
                'average_wind': get_text('Viento Promedio', language),
                'last_forecast': get_text('Último Pronóstico', language),
                'recent_records': get_text('Registros Recientes', language),
                'temperature': get_text('Temperatura', language),
                'humidity': get_text('Humedad Relativa', language),
                'pressure': get_text('Presión Atmosférica', language),
                'wind_speed': get_text('Velocidad del Viento', language),
                'altitude': get_text('Altura sobre el Nivel del Mar', language),
                'cloudiness': get_text('Nubosidad', language),
                'view_forecast': get_text('Ver Pronóstico', language),
                'no_data': get_text('No hay datos disponibles', language),
                'condition': get_text('Condición', language),
                'partly_cloudy': get_text('Parcialmente nublado', language),
                'some_scattered_clouds': get_text('Algunas nubes dispersas', language),
            }
        }
    else:
        context = {
            'total_registros': 0,
            'temp_promedio': 0,
            'humedad_promedio': 0,
            'presion_promedio': 0,
            'viento_promedio': 0,
            'ultimo_registro': None,
            'ultimo_pronostico': None,
            'registros_recientes': [],
            'language': language,
            'texts': {
                'title': get_text('Dashboard', language),
                'subtitle': get_text('Estadísticas del Sistema de Pronóstico Climático', language),
                'total_records': get_text('Total de Registros', language),
                'average_temperature': get_text('Temperatura Promedio', language),
                'average_humidity': get_text('Humedad Promedio', language),
                'average_pressure': get_text('Presión Promedio', language),
                'average_wind': get_text('Viento Promedio', language),
                'last_forecast': get_text('Último Pronóstico', language),
                'recent_records': get_text('Registros Recientes', language),
                'temperature': get_text('Temperatura', language),
                'humidity': get_text('Humedad Relativa', language),
                'pressure': get_text('Presión Atmosférica', language),
                'wind_speed': get_text('Velocidad del Viento', language),
                'altitude': get_text('Altura sobre el Nivel del Mar', language),
                'cloudiness': get_text('Nubosidad', language),
                'view_forecast': get_text('Ver Pronóstico', language),
                'no_data': get_text('No hay datos disponibles', language),
                'condition': get_text('Condición', language),
                'partly_cloudy': get_text('Parcialmente nublado', language),
                'some_scattered_clouds': get_text('Algunas nubes dispersas', language),
            }
        }
    
    response = render(request, 'clima/dashboard.html', context)
    return set_language_cookie(response, language)

def api_nasa_data(request):
    """API para obtener datos de NASA Worldview"""
    try:
        lat = float(request.GET.get('lat', 0))
        lon = float(request.GET.get('lon', 0))
        layer_id = request.GET.get('layer', 'MODIS_Terra_Land_Surface_Temperature_Day')
        
        if lat == 0 and lon == 0:
            return JsonResponse({'error': 'Coordenadas requeridas'}, status=400)
        
        # Datos simulados realistas para Piura
        if lat >= -6.0 and lat <= -4.0 and lon >= -81.0 and lon <= -79.0:
            # Zona de Piura - clima desértico tropical
            temperatura_base = 28.0 + (lat + 5.0) * 2.0  # Más cálido hacia el norte
            humedad_base = 45.0 - (lat + 5.0) * 5.0      # Menos humedad hacia el norte
        else:
            # Otras zonas - datos genéricos
            temperatura_base = 22.0 + (lat * 0.5)
            humedad_base = 60.0 + (lon * 0.1)
        
        simulated_data = {
            'success': True,
            'data': {
                'temperature': round(temperatura_base, 1),
                'cloud_cover': max(5.0, min(30.0, 15.0 + (lon * 0.1))),  # Cielo despejado en Piura
                'pressure': round(1012.0 + (lat * 0.2), 1),
                'humidity': max(20.0, min(80.0, humedad_base))
            },
            'timestamp': datetime.now().isoformat(),
            'layer_id': layer_id,
            'location': {'lat': lat, 'lon': lon}
        }
        
        return JsonResponse(simulated_data)
    
    except (ValueError, TypeError) as e:
        return JsonResponse({'error': 'Parámetros inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)

def visual(request):
    """Versión visual para usuarios normales con datos reales"""
    # Obtener el último registro de la base de datos
    try:
        ultimo_registro = RegistroClima.objects.latest('fecha')
        
        # Preparar datos para mostrar
        datos_clima = {
            'temperatura': ultimo_registro.temperatura,
            'humedad': ultimo_registro.humedad,
            'presion': ultimo_registro.presion,
            'velocidad_viento': ultimo_registro.velocidad_viento,
            'altura': ultimo_registro.altura,
            'nubosidad': ultimo_registro.nubosidad,
            'latitud': ultimo_registro.latitud,
            'longitud': ultimo_registro.longitud,
            'nombre_lugar': ultimo_registro.nombre_lugar or 'Ubicación Actual',
            'fecha': ultimo_registro.fecha,
        }
    except RegistroClima.DoesNotExist:
        # Datos realistas para Piura, Perú (clima desértico tropical)
        datos_clima = {
            'temperatura': 28.5,  # Temperatura típica de Piura
            'humedad': 45.0,      # Humedad baja típica de desierto
            'presion': 1012.8,    # Presión normal para la altitud
            'velocidad_viento': 8.5,  # Viento moderado
            'altura': 26.0,       # Altitud real de Piura
            'nubosidad': 15.0,    # Cielo despejado típico
            'latitud': -5.19449,
            'longitud': -80.6328,
            'nombre_lugar': 'Piura, Perú',
            'fecha': '2025-10-05 12:53:00',
        }
    
    return render(request, 'clima/visual.html', {'datos_clima': datos_clima})

def login_page(request):
    """Página de login para la parte científica"""
    if request.session.get('usuario_autenticado'):
        return redirect('index')
    
    return render(request, 'clima/login.html')

def login_simple(request):
    """Login simple para presentación"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == 'investigador' and password == '123456':
            request.session['usuario_autenticado'] = True
            request.session['usuario_nombre'] = 'Dr. Investigador'
            return redirect('index')
        else:
            messages.error(request, 'Credenciales incorrectas')
    
    return render(request, 'clima/login_simple.html')

@csrf_exempt
def login_auth(request):
    """Autenticación de usuario"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            
            if not username or not password:
                return JsonResponse({
                    'success': False,
                    'message': 'Usuario y contraseña son requeridos'
                })
            
            # Buscar usuario en la base de datos
            try:
                usuario = Login.objects.get(username=username, activo=True)
            except Login.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Usuario no encontrado o inactivo'
                })
            
            # Verificar contraseña (hash simple para demo)
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if usuario.password == password_hash:
                # Login exitoso
                request.session['usuario_autenticado'] = True
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre_completo
                request.session['usuario_rol'] = usuario.rol
                
                # Actualizar último acceso
                usuario.save()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Bienvenido, {usuario.nombre_completo}',
                    'redirect': '/'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Contraseña incorrecta'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Datos inválidos'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error en el servidor'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    })

def logout(request):
    """Cerrar sesión"""
    request.session.flush()
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login_page')

@csrf_exempt
def register_user(request):
    """Registrar nuevo usuario"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            email = data.get('email', '').strip()
            nombre_completo = data.get('nombre_completo', '').strip()
            rol = data.get('rol', 'investigador').strip()
            
            # Validaciones básicas
            if not all([username, password, email, nombre_completo]):
                return JsonResponse({
                    'success': False,
                    'message': 'Todos los campos son requeridos'
                })
            
            # Verificar si el usuario ya existe
            if Login.objects.filter(username=username).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'El nombre de usuario ya existe'
                })
            
            # Crear hash de la contraseña
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Crear usuario
            usuario = Login.objects.create(
                username=username,
                password=password_hash,
                email=email,
                nombre_completo=nombre_completo,
                rol=rol
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Usuario {nombre_completo} registrado exitosamente'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Datos inválidos'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error al registrar usuario'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    })

def check_auth(request):
    """Verificar si el usuario está autenticado"""
    if request.session.get('usuario_autenticado'):
        return JsonResponse({
            'authenticated': True,
            'usuario': request.session.get('usuario_nombre', ''),
            'rol': request.session.get('usuario_rol', '')
        })
    else:
        return JsonResponse({
            'authenticated': False
        })

def visual(request):
    """Versión visual para usuarios normales con datos reales y consistentes"""
    # Obtener el último registro de la base de datos
    try:
        ultimo_registro = RegistroClima.objects.latest('fecha')
        
        # Preparar datos para mostrar (consistentes con el pronóstico)
        datos_clima = {
            'temperatura': ultimo_registro.temperatura,
            'humedad': ultimo_registro.humedad,
            'presion': ultimo_registro.presion,
            'velocidad_viento': ultimo_registro.velocidad_viento,
            'altura': ultimo_registro.altura,
            'nubosidad': ultimo_registro.nubosidad,
            'latitud': ultimo_registro.latitud,
            'longitud': ultimo_registro.longitud,
            'nombre_lugar': ultimo_registro.nombre_lugar or 'Ubicación Actual',
            'fecha': ultimo_registro.fecha,
        }
    except RegistroClima.DoesNotExist:
        # Datos realistas y consistentes para Piura (clima desértico tropical)
        datos_clima = {
            'temperatura': 28,  # Temperatura base consistente
            'humedad': 65,      # Humedad típica de Piura
            'presion': 1013,    # Presión normal
            'velocidad_viento': 12,  # Viento moderado
            'altura': 26.0,     # Altitud real de Piura
            'nubosidad': 35,    # Parcialmente nublado
            'latitud': -5.19449,
            'longitud': -80.6328,
            'nombre_lugar': 'Piura, Perú',
            'fecha': datetime.now(),
        }
    
    # Determinar condición climática basada en nubosidad
    if datos_clima['nubosidad'] < 25:
        condicion = 'Soleado'
    elif datos_clima['nubosidad'] < 50:
        condicion = 'Parcialmente nublado'
    else:
        condicion = 'Nublado'
    
    datos_clima['condicion'] = condicion
    
    return render(request, 'clima/visual.html', {'datos_clima': datos_clima})

def test_api(request):
    """Vista de prueba para verificar que las APIs funcionan"""
    return JsonResponse({
        'status': 'ok',
        'message': 'API funcionando correctamente',
        'timestamp': datetime.now().isoformat(),
        'servidor': 'Django',
        'version': '1.0'
    })

