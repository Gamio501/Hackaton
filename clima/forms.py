from django import forms
from .models import RegistroClima
from .translation_utils import get_text

def create_registro_clima_form(language='en'):
    """
    Crear formulario con traducciones dinámicas
    """
    class RegistroClimaForm(forms.ModelForm):
        ubicacion = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': get_text('Buscar ubicación en el mapa...', language),
                'id': 'ubicacion-input'
            }),
            label=get_text('Buscar Ubicación', language),
            help_text=get_text('Busca una ubicación o haz clic en el mapa para seleccionar', language)
        )
        
        nombre_lugar = forms.CharField(
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': get_text('Ej: Lima, Perú', language),
                'id': 'nombre-lugar-input'
            }),
            label=get_text('Nombre del Lugar', language),
            help_text=get_text('Nombre de la ciudad o lugar donde se realizó el cálculo', language)
        )
        
        class Meta:
            model = RegistroClima
            fields = '__all__'
            widgets = {
                'temperatura': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.1',
                    'placeholder': get_text('Ej: 25.5', language)
                }),
                'humedad': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.1',
                    'min': '0',
                    'max': '100',
                    'placeholder': get_text('Ej: 65.0', language)
                }),
                'presion': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.1',
                    'placeholder': get_text('Ej: 1013.25', language)
                }),
                'velocidad_viento': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.1',
                    'placeholder': get_text('Ej: 15.0', language)
                }),
                'altura': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.1',
                    'placeholder': get_text('Ej: 100.0', language)
                }),
                'nubosidad': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.1',
                    'min': '0',
                    'max': '100',
                    'placeholder': get_text('Ej: 30.0', language)
                }),
                'latitud': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.000001',
                    'min': '-90',
                    'max': '90',
                    'placeholder': get_text('Se llena automáticamente o ingresa manualmente', language),
                    'id': 'latitud-input'
                }),
                'longitud': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.000001',
                    'min': '-180',
                    'max': '180',
                    'placeholder': get_text('Se llena automáticamente o ingresa manualmente', language),
                    'id': 'longitud-input'
                }),
                # Campos de aerosoles y polvo atmosférico
                'densidad_polvo': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.001',
                    'min': '0',
                    'placeholder': get_text('Ej: 15.5', language)
                }),
                'pm25': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.001',
                    'min': '0',
                    'placeholder': get_text('Ej: 12.3', language)
                }),
                'pm10': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.001',
                    'min': '0',
                    'placeholder': get_text('Ej: 25.7', language)
                }),
                'diametro_medio': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.001',
                    'min': '0',
                    'placeholder': get_text('Ej: 2.1', language)
                }),
                'desviacion_diametro': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.001',
                    'min': '0',
                    'placeholder': get_text('Ej: 0.8', language)
                }),
                'aod': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.000001',
                    'min': '0',
                    'placeholder': get_text('Ej: 0.15', language)
                }),
                'visibilidad': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.1',
                    'min': '0',
                    'placeholder': get_text('Ej: 10.5', language)
                }),
                'altura_capa_mezcla': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.1',
                    'min': '0',
                    'placeholder': get_text('Ej: 1200.0', language)
                }),
            }
            labels = {
                'temperatura': get_text('Temperatura', language) + (' (°F)' if language == 'en' else ' (°C)'),
                'humedad': get_text('Humedad Relativa', language) + ' (%)',
                'presion': get_text('Presión Atmosférica', language) + ' (hPa)',
                'velocidad_viento': get_text('Velocidad del Viento', language) + (' (mph)' if language == 'en' else ' (km/h)'),
                'altura': get_text('Altura sobre el Nivel del Mar', language) + (' (ft)' if language == 'en' else ' (m)'),
                'nubosidad': get_text('Nubosidad', language) + ' (%)',
                'latitud': get_text('Latitud', language),
                'longitud': get_text('Longitud', language),
                # Labels para aerosoles
                'densidad_polvo': get_text('Densidad de Polvo', language) + ' (µg/m³)',
                'pm25': 'PM2.5 (µg/m³)',
                'pm10': 'PM10 (µg/m³)',
                'diametro_medio': get_text('Diámetro Medio', language) + ' (µm)',
                'desviacion_diametro': get_text('Desviación del Diámetro', language) + ' (µm)',
                'aod': get_text('Profundidad Óptica de Aerosoles', language) + ' (AOD)',
                'visibilidad': get_text('Visibilidad', language) + (' (mi)' if language == 'en' else ' (km)'),
                'altura_capa_mezcla': get_text('Altura de la Capa de Mezcla', language) + (' (ft)' if language == 'en' else ' (m)'),
            }
            help_texts = {
                'temperatura': get_text('Ingrese la temperatura en grados Celsius', language),
                'humedad': get_text('Ingrese la humedad relativa (0-100%)', language),
                'presion': get_text('Ingrese la presión atmosférica en hectopascales', language),
                'velocidad_viento': get_text('Ingrese la velocidad del viento en km/h', language),
                'altura': get_text('Ingrese la altura sobre el nivel del mar en metros', language),
                'nubosidad': get_text('Ingrese el porcentaje de nubosidad (0-100%)', language),
                'latitud': get_text('Se llena automáticamente o puedes editarlo manualmente', language),
                'longitud': get_text('Se llena automáticamente o puedes editarlo manualmente', language),
                # Help texts para aerosoles
                'densidad_polvo': get_text('Densidad de partículas de polvo en microgramos por metro cúbico', language),
                'pm25': get_text('Concentración de partículas menores a 2.5 micrómetros', language),
                'pm10': get_text('Concentración de partículas menores a 10 micrómetros', language),
                'diametro_medio': get_text('Diámetro promedio de las partículas en micrómetros', language),
                'desviacion_diametro': get_text('Desviación estándar del diámetro de partículas', language),
                'aod': get_text('Profundidad óptica de aerosoles (adimensional)', language),
                'visibilidad': get_text('Visibilidad atmosférica en kilómetros', language),
                'altura_capa_mezcla': get_text('Altura de la capa de mezcla atmosférica en metros', language),
            }
    
    return RegistroClimaForm

class RegistroClimaForm(forms.ModelForm):
    ubicacion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar ubicación en el mapa...',
            'id': 'ubicacion-input'
        }),
        label='Buscar Ubicación',
        help_text='Busca una ubicación o haz clic en el mapa para seleccionar'
    )
    
    class Meta:
        model = RegistroClima
        fields = '__all__'
        widgets = {
            'temperatura': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Ej: 25.5'
            }),
            'humedad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '100',
                'placeholder': 'Ej: 65.0'
            }),
            'presion': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Ej: 1013.25'
            }),
            'velocidad_viento': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Ej: 15.0'
            }),
            'altura': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Ej: 100.0'
            }),
            'nubosidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'max': '100',
                'placeholder': 'Ej: 30.0'
            }),
            'latitud': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'min': '-90',
                'max': '90',
                'placeholder': 'Se llena automáticamente o ingresa manualmente',
                'id': 'latitud-input'
            }),
            'longitud': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'min': '-180',
                'max': '180',
                'placeholder': 'Se llena automáticamente o ingresa manualmente',
                'id': 'longitud-input'
            }),
            # Campos de aerosoles y polvo atmosférico
            'densidad_polvo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0',
                'placeholder': 'Ej: 15.5'
            }),
            'pm25': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0',
                'placeholder': 'Ej: 12.3'
            }),
            'pm10': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0',
                'placeholder': 'Ej: 25.7'
            }),
            'diametro_medio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0',
                'placeholder': 'Ej: 2.1'
            }),
            'desviacion_diametro': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.001',
                'min': '0',
                'placeholder': 'Ej: 0.8'
            }),
            'aod': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'min': '0',
                'placeholder': 'Ej: 0.15'
            }),
            'visibilidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Ej: 10.5'
            }),
            'altura_capa_mezcla': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0',
                'placeholder': 'Ej: 1200.0'
            }),
        }
        labels = {
            'temperatura': 'Temperatura (°C)',
            'humedad': 'Humedad Relativa (%)',
            'presion': 'Presión Atmosférica (hPa)',
            'velocidad_viento': 'Velocidad del Viento (km/h)',
            'altura': 'Altura sobre el Nivel del Mar (m)',
            'nubosidad': 'Nubosidad (%)',
            'latitud': 'Latitud',
            'longitud': 'Longitud',
            # Labels para aerosoles
            'densidad_polvo': 'Densidad del Polvo (µg/m³)',
            'pm25': 'PM2.5 (µg/m³)',
            'pm10': 'PM10 (µg/m³)',
            'diametro_medio': 'Diámetro Medio (µm)',
            'desviacion_diametro': 'Desviación Diámetro (µm)',
            'aod': 'Profundidad Óptica Aerosoles (AOD)',
            'visibilidad': 'Visibilidad (km)',
            'altura_capa_mezcla': 'Altura Capa Mezcla (m)',
        }
        help_texts = {
            'temperatura': 'Ingrese la temperatura en grados Celsius',
            'humedad': 'Ingrese la humedad relativa (0-100%)',
            'presion': 'Ingrese la presión atmosférica en hectopascales',
            'velocidad_viento': 'Ingrese la velocidad del viento en km/h',
            'altura': 'Ingrese la altura sobre el nivel del mar en metros',
            'nubosidad': 'Ingrese el porcentaje de nubosidad (0-100%)',
            'latitud': 'Se llena automáticamente o puedes editarlo manualmente',
            'longitud': 'Se llena automáticamente o puedes editarlo manualmente',
            # Help texts para aerosoles
            'densidad_polvo': 'Densidad de partículas de polvo en microgramos por metro cúbico',
            'pm25': 'Concentración de partículas menores a 2.5 micrómetros',
            'pm10': 'Concentración de partículas menores a 10 micrómetros',
            'diametro_medio': 'Diámetro promedio de las partículas en micrómetros',
            'desviacion_diametro': 'Desviación estándar del diámetro de partículas',
            'aod': 'Profundidad óptica de aerosoles (adimensional)',
            'visibilidad': 'Visibilidad atmosférica en kilómetros',
            'altura_capa_mezcla': 'Altura de la capa de mezcla atmosférica en metros',
        }