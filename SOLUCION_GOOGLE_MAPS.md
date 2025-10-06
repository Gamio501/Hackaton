# 🔧 Solución para el Error de Google Maps

## ❌ **Problema Actual**
El error "Se produjo un error. Esta página no cargó bien Google Maps" se debe a que no tienes configurada la API key de Google Maps.

## ✅ **Solución Rápida: Usar OpenStreetMap**

### **Acceder a la versión sin API Key:**
```
http://127.0.0.1:8000/osm/
```

**Ventajas:**
- ✅ Funciona inmediatamente
- ✅ Sin configuración
- ✅ Completamente gratuito
- ✅ Mismas funcionalidades

---

## 🔑 **Solución Alternativa: Configurar Google Maps**

### **Paso 1: Obtener API Key Gratuita**
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto o selecciona uno existente
3. Habilita las APIs:
   - Maps JavaScript API
   - Places API
4. Crea credenciales (API Key)

### **Paso 2: Configurar en el Proyecto**
1. Abre el archivo `templates/clima/index.html`
2. Busca esta línea:
   ```html
   src="https://maps.googleapis.com/maps/api/js?key=TU_API_KEY_AQUI&libraries=places&callback=initMap">
   ```
3. Reemplaza `TU_API_KEY_AQUI` con tu clave real

### **Paso 3: Verificar**
- Accede a: `http://127.0.0.1:8000/`
- El mapa de Google Maps debería funcionar

---

## 🎯 **Recomendación**

**Para desarrollo y pruebas:**
- **Usa OpenStreetMap** (`/osm/`) - Funciona inmediatamente

**Para producción:**
- **Google Maps** - Mejor calidad pero requiere API key
- **OpenStreetMap** - Gratuito y confiable

---

## 🚀 **Acceso Inmediato**

**Sin configuración:**
```
http://127.0.0.1:8000/osm/
```

**Con Google Maps (requiere API key):**
```
http://127.0.0.1:8000/
```

¡Ambas versiones tienen las mismas funcionalidades!
