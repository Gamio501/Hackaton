# 🗺️ Configuración de Google Maps API

## 📋 Pasos para Obtener tu API Key

### 1. Crear una Cuenta en Google Cloud Platform
- Ve a [Google Cloud Console](https://console.cloud.google.com/)
- Inicia sesión con tu cuenta de Google
- Acepta los términos de servicio

### 2. Crear un Proyecto
- Haz clic en "Seleccionar proyecto" en la parte superior
- Haz clic en "Nuevo proyecto"
- Ingresa un nombre para tu proyecto (ej: "Pronostico Clima")
- Haz clic en "Crear"

### 3. Habilitar las APIs Necesarias
- En el menú lateral, ve a "APIs y servicios" > "Biblioteca"
- Busca y habilita las siguientes APIs:
  - **Maps JavaScript API**
  - **Places API**
  - **Geocoding API** (opcional, para obtener direcciones)

### 4. Crear Credenciales (API Key)
- Ve a "APIs y servicios" > "Credenciales"
- Haz clic en "Crear credenciales" > "Clave de API"
- Copia la clave generada

### 5. Configurar Restricciones (Recomendado)
- Haz clic en la clave de API creada
- En "Restricciones de aplicación":
  - **Restricciones de sitio web HTTP**: Agrega tu dominio
  - **Restricciones de IP**: Agrega tu IP local (127.0.0.1)
- En "Restricciones de API":
  - Selecciona solo las APIs que necesitas

## 🔧 Configuración en el Proyecto

### Opción 1: Configuración Simple
1. Abre el archivo `templates/clima/index.html`
2. Busca la línea:
   ```html
   src="https://maps.googleapis.com/maps/api/js?key=TU_API_KEY_AQUI&libraries=places&callback=initMap">
   ```
3. Reemplaza `TU_API_KEY_AQUI` con tu clave real

### Opción 2: Configuración Avanzada
1. Abre `clima/google_maps_config.py`
2. Reemplaza `TU_API_KEY_AQUI` con tu clave real
3. Modifica `templates/clima/index.html` para usar la configuración:

```html
<script async defer 
    src="https://maps.googleapis.com/maps/api/js?key={{ GOOGLE_MAPS_API_KEY }}&libraries=places&callback=initMap">
</script>
```

## 💰 Costos y Límites

### Límites Gratuitos (Cada mes)
- **Maps JavaScript API**: 28,000 cargas de mapa
- **Places API**: 1,000 solicitudes
- **Geocoding API**: 40,000 solicitudes

### Para Desarrollo Local
- Los límites gratuitos son más que suficientes
- No se requiere tarjeta de crédito para empezar

## 🚀 Funcionalidades Implementadas

### ✅ Búsqueda de Ubicaciones
- Campo de búsqueda integrado
- Autocompletado de lugares
- Búsqueda por dirección, ciudad, país

### ✅ Selección Visual
- Clic en el mapa para seleccionar ubicación
- Marcador arrastrable
- Coordenadas automáticas

### ✅ Geocodificación
- Conversión de coordenadas a dirección
- Dirección automática al hacer clic
- Actualización en tiempo real

## 🔒 Seguridad

### Restricciones Recomendadas
1. **Restricciones de sitio web**: Solo tu dominio
2. **Restricciones de API**: Solo APIs necesarias
3. **Restricciones de IP**: Solo IPs autorizadas

### Para Desarrollo
- Usa `localhost` y `127.0.0.1` en restricciones
- No expongas la clave en repositorios públicos

## 🐛 Solución de Problemas

### Error: "This page can't load Google Maps correctly"
- Verifica que la API key sea correcta
- Asegúrate de que las APIs estén habilitadas
- Revisa las restricciones de la clave

### Error: "RefererNotAllowedMapError"
- Agrega tu dominio a las restricciones de sitio web
- O elimina las restricciones temporalmente para desarrollo

### El mapa no se carga
- Verifica la consola del navegador para errores
- Asegúrate de que la API key tenga permisos para Maps JavaScript API

## 📞 Soporte

- [Documentación de Google Maps](https://developers.google.com/maps/documentation)
- [Google Cloud Support](https://cloud.google.com/support)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-maps-api)

---

**¡Una vez configurado, tendrás un mapa interactivo completamente funcional! 🗺️✨**
