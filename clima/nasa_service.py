import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class NASADataService:
    """
    Servicio para obtener datos de la API de NASA Worldview/GIBS
    """
    
    def __init__(self):
        self.base_url = "https://gibs.earthdata.nasa.gov"
        self.wmts_url = f"{self.base_url}/wmts/epsg4326/best"
        self.wms_url = f"{self.base_url}/wms/epsg4326/best"
        
    def get_satellite_data(self, lat: float, lon: float, layer_id: str = 'MODIS_Terra_Land_Surface_Temperature_Day') -> Dict:
        """
        Obtiene datos satelitales para una ubicación específica
        
        Args:
            lat (float): Latitud
            lon (float): Longitud
            layer_id (str): ID de la capa de datos
            
        Returns:
            Dict: Datos satelitales procesados
        """
        try:
            # Obtener fecha actual
            today = datetime.now()
            
            # Construir URL para obtener datos
            url = self._build_data_url(layer_id, today)
            
            # Simular datos (en una implementación real, harías una llamada HTTP)
            # Por ahora, generamos datos simulados basados en la ubicación
            data = self._simulate_satellite_data(lat, lon, layer_id)
            
            return {
                'success': True,
                'data': data,
                'timestamp': today.isoformat(),
                'layer_id': layer_id,
                'location': {'lat': lat, 'lon': lon}
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo datos satelitales: {e}")
            return {
                'success': False,
                'error': str(e),
                'data': None
            }
    
    def _build_data_url(self, layer_id: str, date: datetime) -> str:
        """
        Construye la URL para obtener datos de una capa específica
        
        Args:
            layer_id (str): ID de la capa
            date (datetime): Fecha para los datos
            
        Returns:
            str: URL construida
        """
        date_str = date.strftime('%Y-%m-%d')
        return f"{self.wmts_url}/{layer_id}/default/{date_str}/250m/{{z}}/{{y}}/{{x}}.png"
    
    def _simulate_satellite_data(self, lat: float, lon: float, layer_id: str) -> Dict:
        """
        Simula datos satelitales basados en la ubicación y tipo de capa
        
        Args:
            lat (float): Latitud
            lon (float): Longitud
            layer_id (str): ID de la capa
            
        Returns:
            Dict: Datos simulados
        """
        # Factores de simulación basados en ubicación geográfica
        lat_factor = abs(lat) / 90.0  # 0 a 1
        lon_factor = (lon + 180) / 360.0  # 0 a 1
        
        # Simular datos según el tipo de capa
        if 'Temperature' in layer_id:
            # Temperatura basada en latitud y estación
            base_temp = 30 - (lat_factor * 40)  # Más frío hacia los polos
            temp_variation = (lat_factor + lon_factor) * 10
            temperature = base_temp + temp_variation
            
            return {
                'temperature': round(temperature, 1),
                'unit': '°C',
                'description': 'Temperatura de superficie terrestre'
            }
            
        elif 'Cloud' in layer_id:
            # Datos de nubes
            cloud_fraction = (lat_factor + lon_factor) * 50
            cloud_height = 2 + (lat_factor * 8)  # 2-10 km
            
            return {
                'cloud_fraction': round(cloud_fraction, 1),
                'cloud_height': round(cloud_height, 1),
                'unit': '%',
                'description': 'Datos de cobertura nubosa'
            }
            
        elif 'Aerosol' in layer_id:
            # Datos de aerosoles
            aerosol_optical_depth = 0.1 + (lat_factor * 0.5)
            
            return {
                'aerosol_optical_depth': round(aerosol_optical_depth, 3),
                'description': 'Profundidad óptica de aerosoles'
            }
            
        elif 'Water_Vapor' in layer_id:
            # Vapor de agua
            water_vapor = 1.0 + (lat_factor * 3.0)
            
            return {
                'water_vapor': round(water_vapor, 2),
                'unit': 'g/cm²',
                'description': 'Contenido de vapor de agua'
            }
            
        else:
            # Datos genéricos
            return {
                'value': round((lat_factor + lon_factor) * 100, 2),
                'description': 'Datos satelitales generales'
            }
    
    def get_multiple_layers_data(self, lat: float, lon: float, layer_ids: List[str]) -> Dict:
        """
        Obtiene datos de múltiples capas para una ubicación
        
        Args:
            lat (float): Latitud
            lon (float): Longitud
            layer_ids (List[str]): Lista de IDs de capas
            
        Returns:
            Dict: Datos de todas las capas
        """
        results = {}
        
        for layer_id in layer_ids:
            data = self.get_satellite_data(lat, lon, layer_id)
            results[layer_id] = data
        
        return results
    
    def get_weather_summary(self, lat: float, lon: float) -> Dict:
        """
        Obtiene un resumen meteorológico basado en datos satelitales
        
        Args:
            lat (float): Latitud
            lon (float): Longitud
            
        Returns:
            Dict: Resumen meteorológico
        """
        # Obtener datos de múltiples capas relevantes
        layer_ids = [
            'MODIS_Terra_Land_Surface_Temperature_Day',
            'MODIS_Terra_Cloud_Fraction',
            'MODIS_Terra_Water_Vapor',
            'MODIS_Terra_Aerosol_Optical_Depth'
        ]
        
        data = self.get_multiple_layers_data(lat, lon, layer_ids)
        
        # Procesar y resumir los datos
        summary = {
            'location': {'lat': lat, 'lon': lon},
            'timestamp': datetime.now().isoformat(),
            'weather_conditions': self._analyze_weather_conditions(data),
            'recommendations': self._generate_recommendations(data),
            'raw_data': data
        }
        
        return summary
    
    def _analyze_weather_conditions(self, data: Dict) -> Dict:
        """
        Analiza las condiciones meteorológicas basadas en datos satelitales
        
        Args:
            data (Dict): Datos de múltiples capas
            
        Returns:
            Dict: Análisis de condiciones meteorológicas
        """
        conditions = {
            'sky_condition': 'Desconocido',
            'precipitation_probability': 0,
            'visibility': 'Buena',
            'air_quality': 'Buena'
        }
        
        # Analizar datos de nubes
        if 'MODIS_Terra_Cloud_Fraction' in data and data['MODIS_Terra_Cloud_Fraction']['success']:
            cloud_data = data['MODIS_Terra_Cloud_Fraction']['data']
            if 'cloud_fraction' in cloud_data:
                cloud_fraction = cloud_data['cloud_fraction']
                if cloud_fraction < 25:
                    conditions['sky_condition'] = 'Despejado'
                elif cloud_fraction < 50:
                    conditions['sky_condition'] = 'Parcialmente nublado'
                elif cloud_fraction < 75:
                    conditions['sky_condition'] = 'Nublado'
                else:
                    conditions['sky_condition'] = 'Muy nublado'
                
                # Estimar probabilidad de precipitación
                conditions['precipitation_probability'] = min(cloud_fraction * 0.8, 90)
        
        # Analizar calidad del aire
        if 'MODIS_Terra_Aerosol_Optical_Depth' in data and data['MODIS_Terra_Aerosol_Optical_Depth']['success']:
            aerosol_data = data['MODIS_Terra_Aerosol_Optical_Depth']['data']
            if 'aerosol_optical_depth' in aerosol_data:
                aod = aerosol_data['aerosol_optical_depth']
                if aod < 0.2:
                    conditions['air_quality'] = 'Excelente'
                elif aod < 0.4:
                    conditions['air_quality'] = 'Buena'
                elif aod < 0.6:
                    conditions['air_quality'] = 'Moderada'
                else:
                    conditions['air_quality'] = 'Pobre'
        
        return conditions
    
    def _generate_recommendations(self, data: Dict) -> List[str]:
        """
        Genera recomendaciones basadas en los datos satelitales
        
        Args:
            data (Dict): Datos de múltiples capas
            
        Returns:
            List[str]: Lista de recomendaciones
        """
        recommendations = []
        
        # Analizar temperatura
        if 'MODIS_Terra_Land_Surface_Temperature_Day' in data and data['MODIS_Terra_Land_Surface_Temperature_Day']['success']:
            temp_data = data['MODIS_Terra_Land_Surface_Temperature_Day']['data']
            if 'temperature' in temp_data:
                temp = temp_data['temperature']
                if temp > 35:
                    recommendations.append("Temperatura muy alta - Mantente hidratado y busca sombra")
                elif temp < 5:
                    recommendations.append("Temperatura muy baja - Abrígate bien")
        
        # Analizar nubes
        if 'MODIS_Terra_Cloud_Fraction' in data and data['MODIS_Terra_Cloud_Fraction']['success']:
            cloud_data = data['MODIS_Terra_Cloud_Fraction']['data']
            if 'cloud_fraction' in cloud_data:
                cloud_fraction = cloud_data['cloud_fraction']
                if cloud_fraction > 80:
                    recommendations.append("Cielo muy nublado - Posible lluvia")
                elif cloud_fraction < 20:
                    recommendations.append("Cielo despejado - Protección solar recomendada")
        
        # Analizar calidad del aire
        if 'MODIS_Terra_Aerosol_Optical_Depth' in data and data['MODIS_Terra_Aerosol_Optical_Depth']['success']:
            aerosol_data = data['MODIS_Terra_Aerosol_Optical_Depth']['data']
            if 'aerosol_optical_depth' in aerosol_data:
                aod = aerosol_data['aerosol_optical_depth']
                if aod > 0.6:
                    recommendations.append("Calidad del aire pobre - Evita actividades al aire libre")
        
        return recommendations

# Instancia global del servicio
nasa_service = NASADataService()
