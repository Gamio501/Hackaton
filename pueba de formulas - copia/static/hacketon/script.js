// Weather App JavaScript
let mobileMap, desktopMap;
let currentLocation = null;
let weatherMarkers = [];
let currentLayer = 'satellite';

// 📦 Control de datos estáticos de horas pasadas
let staticPastHoursData = {};


// OpenWeatherMap API Configuration
const API_KEY = 'e7d9681e303eeef781dc92968e2baa48'; // Replace with your actual API key
const API_BASE_URL = 'https://api.openweathermap.org/data/2.5';

document.addEventListener('DOMContentLoaded', function() {
    // Load static past hours data first
    loadStaticPastHoursData();
    
    // Initialize the app
    initializeApp();
    
    // Add interactive features
    addInteractiveFeatures();
    
    // Initialize maps
    initializeMaps();
    
    // Get user's current location and load weather
    loadCurrentLocationWeather();
    
    // Simulate real-time updates
    startRealTimeUpdates();
    
    // Initialize enhanced radar
    initializeEnhancedRadar();
});

function initializeApp() {
    // Set current time for hourly forecast
    updateCurrentTime();
    
    // Initialize calendar
    initializeCalendar();
    
    // Add loading animation
    addLoadingAnimation();
    
    // Initialize search functionality
    initializeSearch();
}

function addInteractiveFeatures() {
    // Add hover effects to weather details
    const detailItems = document.querySelectorAll('.detail-item, .detail-item-desktop');
    detailItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 15px 40px rgba(0, 0, 0, 0.4)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.3)';
        });
    });
    
    // Add click effects to hourly items
    const hourItems = document.querySelectorAll('.hour-item, .hour-item-desktop');
    hourItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active class from all items
            hourItems.forEach(hourItem => hourItem.classList.remove('active'));
            // Add active class to clicked item
            this.classList.add('active');
            
            // Update main weather display with selected hour data
            updateMainWeatherFromHour(this);
        });
    });
    
    // Add weather report interactions
    addWeatherReportInteractions();
    
    // Add hourly navigation event listeners
    initializeHourlyNavigation();
}

function initializeHourlyNavigation() {
    // Mobile navigation
    const prevMobile = document.querySelector('#hourly-prev');
    const nextMobile = document.querySelector('#hourly-next');
    
    if (prevMobile) {
        prevMobile.addEventListener('click', () => navigateHourly(-1));
    }
    
    if (nextMobile) {
        nextMobile.addEventListener('click', () => navigateHourly(1));
    }
    
    // Desktop navigation
    const prevDesktop = document.querySelector('#hourly-prev-desktop');
    const nextDesktop = document.querySelector('#hourly-next-desktop');
    
    if (prevDesktop) {
        prevDesktop.addEventListener('click', () => navigateHourly(-1));
    }
    
    if (nextDesktop) {
        nextDesktop.addEventListener('click', () => navigateHourly(1));
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            navigateHourly(-1);
        } else if (e.key === 'ArrowRight') {
            navigateHourly(1);
        }
    });
}

function updateCurrentTime() {
    const now = new Date();
    const currentHour = now.getHours();
    
    // Update "Ahora" in hourly forecast
    const nowItems = document.querySelectorAll('.hour-item, .hour-item-desktop');
    nowItems.forEach(item => {
        const hourText = item.querySelector('.hour');
        if (hourText && hourText.textContent === 'Ahora') {
            hourText.textContent = `${currentHour}:00`;
        }
    });
}

function initializeCalendar() {
    // Update calendar immediately
    updateCalendar();
    
    // Update calendar every second
    setInterval(updateCalendar, 1000);
}

function updateCalendar() {
    const now = new Date();
    
    // Format date in Spanish
    const dateOptions = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    const formattedDate = now.toLocaleDateString('es-ES', dateOptions);
    
    // Format time
    const timeOptions = { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
    };
    const formattedTime = now.toLocaleTimeString('es-ES', timeOptions);
    
    // Update mobile calendar
    const mobileDate = document.getElementById('current-date');
    const mobileTime = document.getElementById('current-time');
    if (mobileDate) mobileDate.textContent = formattedDate;
    if (mobileTime) mobileTime.textContent = formattedTime;
    
    // Update desktop calendar
    const desktopDate = document.getElementById('current-date-desktop');
    const desktopTime = document.getElementById('current-time-desktop');
    if (desktopDate) desktopDate.textContent = formattedDate;
    if (desktopTime) desktopTime.textContent = formattedTime;
}

function addLoadingAnimation() {
    // Add loading animation to weather icon
    const weatherIcons = document.querySelectorAll('.weather-icon i, .weather-icon-desktop i');
    weatherIcons.forEach(icon => {
        icon.style.animation = 'float 3s ease-in-out infinite';
    });
}

function initializeSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchBtn = document.querySelector('.search-btn');
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'search-suggestions';
    suggestionsContainer.style.display = 'none';
    
    searchInput.parentNode.appendChild(suggestionsContainer);
    
    // Input event for suggestions
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        if (query.length < 2) {
            suggestionsContainer.style.display = 'none';
            return;
        }
        
        const suggestions = getCitySuggestions(query);
        showSearchSuggestions(suggestions, suggestionsContainer);
    });
    
    // Enter key event for direct search
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const query = this.value.trim();
            if (query.length >= 2) {
                searchLocation(query);
                suggestionsContainer.style.display = 'none';
            }
        }
    });
    
    // Search button click event
    searchBtn.addEventListener('click', function() {
        const query = searchInput.value.trim();
        if (query.length >= 2) {
            searchLocation(query);
            suggestionsContainer.style.display = 'none';
        } else {
            showNotification('Por favor ingresa al menos 2 caracteres', 'warning');
        }
    });
    
    // Blur event to hide suggestions
    searchInput.addEventListener('blur', function() {
        // Hide suggestions after a short delay
        setTimeout(() => {
            suggestionsContainer.style.display = 'none';
        }, 200);
    });
    
    // Focus event to show suggestions if there's text
    searchInput.addEventListener('focus', function() {
        const query = this.value.trim();
        if (query.length >= 2) {
            const suggestions = getCitySuggestions(query);
            showSearchSuggestions(suggestions, suggestionsContainer);
        }
    });
}

function getCitySuggestions(query) {
    const cities = [
        // Ciudades españolas principales
        'Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Zaragoza', 'Málaga', 'Murcia', 'Palma', 'Las Palmas', 'Bilbao',
        'Alicante', 'Córdoba', 'Valladolid', 'Vigo', 'Gijón', 'Hospitalet', 'A Coruña', 'Vitoria', 'Granada', 'Elche',
        'Santa Cruz de Tenerife', 'Oviedo', 'Badalona', 'Cartagena', 'Terrassa', 'Jerez de la Frontera', 'Sabadell', 'Móstoles', 'Alcalá de Henares', 'Pamplona',
        'Fuenlabrada', 'Almería', 'Leganés', 'Santander', 'Castellón de la Plana', 'Burgos', 'Albacete', 'Getafe', 'Salamanca', 'Huelva',
        'Logroño', 'Badajoz', 'San Sebastián', 'León', 'Cádiz', 'Tarragona', 'Lleida', 'Marbella', 'Dos Hermanas', 'Mataró',
        'Santa Coloma de Gramenet', 'Alcorcón', 'Jaén', 'Ourense', 'Reus', 'Torrevieja', 'El Puerto de Santa María', 'Alcoy', 'Cáceres', 'Lugo',
        
        // Ciudades internacionales populares
        'Londres', 'París', 'Roma', 'Berlín', 'Ámsterdam', 'Viena', 'Praga', 'Budapest', 'Varsovia', 'Moscú',
        'Nueva York', 'Los Ángeles', 'Chicago', 'Miami', 'San Francisco', 'Boston', 'Seattle', 'Denver', 'Las Vegas', 'Washington',
        'Ciudad de México', 'Buenos Aires', 'São Paulo', 'Río de Janeiro', 'Lima', 'Bogotá', 'Santiago', 'Caracas', 'Montevideo', 'La Paz',
        'Tokio', 'Pekín', 'Shanghái', 'Hong Kong', 'Singapur', 'Bangkok', 'Yakarta', 'Manila', 'Seúl', 'Osaka',
        'El Cairo', 'Johannesburgo', 'Casablanca', 'Nairobi', 'Lagos', 'Túnez', 'Argel', 'Addis Abeba', 'Dakar', 'Accra',
        'Sídney', 'Melbourne', 'Perth', 'Brisbane', 'Auckland', 'Wellington', 'Christchurch', 'Adelaida', 'Darwin', 'Hobart'
    ];
    
    return cities
        .filter(city => city.toLowerCase().includes(query.toLowerCase()))
        .slice(0, 8);
}

function showSearchSuggestions(suggestions, container) {
    if (suggestions.length === 0) {
        container.style.display = 'none';
        return;
    }
    
    container.innerHTML = suggestions.map(city => `
        <div class="suggestion-item" data-city="${city}">
            <i class="fas fa-map-marker-alt"></i>
            <span>${city}</span>
        </div>
    `).join('');
    
    container.style.display = 'block';
    
    // Add click events to suggestions
    container.querySelectorAll('.suggestion-item').forEach(item => {
        item.addEventListener('click', function() {
            const city = this.dataset.city;
            searchLocation(city);
            container.style.display = 'none';
        });
    });
}

async function searchLocation(location) {
    console.log('🔍 Iniciando búsqueda de:', location);
    
    // Clear search input first
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.value = '';
    }
    
    // Hide search suggestions
    const suggestionsContainer = document.querySelector('.search-suggestions');
    if (suggestionsContainer) {
        suggestionsContainer.style.display = 'none';
    }
    
    // Show loading notification
    showNotification(`Buscando datos de ${location}...`, 'info');
    
    try {
        console.log('🌐 Consultando API de OpenWeatherMap...');
        // Try to get real weather data
        const weatherData = await fetchWeatherData(location);
        console.log('✅ Datos obtenidos:', weatherData);
        
        // Update ALL weather displays with the new city data
        console.log('🔄 Actualizando interfaz...');
        updateMainWeatherFromMap(weatherData);
        
        // Center maps on the searched city
        console.log('🗺️ Centrando mapas en:', weatherData.lat, weatherData.lng);
        centerMapOnCity(weatherData);
        
        // Add search result marker
        if (mobileMap) {
            console.log('📍 Agregando marcador en mapa móvil');
            addSearchResultMarker(mobileMap, weatherData.lat, weatherData.lng, weatherData.name, weatherData.temp, weatherData.description, weatherData.humidity, weatherData.wind);
        }
        if (desktopMap) {
            console.log('📍 Agregando marcador en mapa escritorio');
            addSearchResultMarker(desktopMap, weatherData.lat, weatherData.lng, weatherData.name, weatherData.temp, weatherData.description, weatherData.humidity, weatherData.wind);
        }
        
        showNotification(`✅ Datos de ${weatherData.name} cargados correctamente`, 'success');
        console.log('🎉 Búsqueda completada exitosamente');
        
    } catch (error) {
        console.error('❌ Error fetching weather data:', error);
        showNotification(`❌ Error al obtener datos de ${location}: ${error.message}`, 'error');
        
        // Fallback to simulated data
        console.log('🔄 Usando datos simulados como fallback...');
        const fallbackData = generateLocationWeatherData(location);
        console.log('📊 Datos simulados:', fallbackData);
        
        updateMainWeatherFromMap(fallbackData);
        centerMapOnCity(fallbackData);
        
        // Add search result marker for fallback data
        if (mobileMap) {
            addSearchResultMarker(mobileMap, fallbackData.lat, fallbackData.lng, fallbackData.name, fallbackData.temp, fallbackData.description, fallbackData.humidity, fallbackData.wind);
        }
        if (desktopMap) {
            addSearchResultMarker(desktopMap, fallbackData.lat, fallbackData.lng, fallbackData.name, fallbackData.temp, fallbackData.description, fallbackData.humidity, fallbackData.wind);
        }
        
        showNotification(`⚠️ Mostrando datos simulados para ${location}`, 'warning');
    }
}

function updateMainWeatherLocation(location) {
    // Update mobile main location
    const mobileLocation = document.getElementById('main-location');
    if (mobileLocation) {
        const span = mobileLocation.querySelector('span');
        if (span) {
            span.textContent = location;
        }
    }
    
    // Update desktop main location
    const desktopLocation = document.getElementById('main-location-desktop');
    if (desktopLocation) {
        const span = desktopLocation.querySelector('span');
        if (span) {
            span.textContent = location;
        }
    }
}

async function updateWeatherData(location) {
    // Show loading notification
    showNotification('Obteniendo datos del clima...', 'info');
    
    try {
        const weatherData = await fetchWeatherData(location);
        updateMainWeatherFromMap(weatherData);
        centerMapOnCity(weatherData);
        showNotification('Datos del clima actualizados', 'success');
    } catch (error) {
        console.error('Error fetching weather data:', error);
        showNotification('Error al obtener datos del clima', 'error');
        
        // Fallback to simulated data
        const fallbackData = generateLocationWeatherData(location);
        updateMainWeatherFromMap(fallbackData);
        centerMapOnCity(fallbackData);
    }
}

async function fetchWeatherData(location) {
    console.log('🔑 API Key configurada:', API_KEY !== 'TU_API_KEY' ? 'Sí' : 'No');
    
    // Check if API key is configured
    if (API_KEY === 'TU_API_KEY') {
        throw new Error('API key not configured');
    }
    
    const url = `${API_BASE_URL}/weather?q=${encodeURIComponent(location)}&appid=${API_KEY}&units=metric&lang=es`;
    console.log('🌐 URL de la API:', url);
    
    try {
        const response = await fetch(url);
        console.log('📡 Respuesta de la API:', response.status, response.statusText);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error('❌ Error de la API:', errorData);
            throw new Error(`HTTP error! status: ${response.status} - ${errorData.message || response.statusText}`);
        }
        
        const data = await response.json();
        console.log('📊 Datos de la API:', data);
        
        // Transform API data to our format
        const transformedData = {
            name: data.name + ', ' + data.sys.country,
            lat: data.coord.lat,
            lng: data.coord.lon,
            temp: Math.round(data.main.temp),
            description: data.weather[0].description,
            humidity: data.main.humidity,
            wind: Math.round(data.wind.speed * 3.6), // Convert m/s to km/h
            uv: 0, // UV index not available in current weather API
            visibility: Math.round(data.visibility / 1000), // Convert m to km
            pressure: data.main.pressure,
            feelsLike: Math.round(data.main.feels_like),
            country: data.sys.country,
            weatherIcon: data.weather[0].icon
        };
        
        console.log('✅ Datos transformados:', transformedData);
        return transformedData;
        
    } catch (error) {
        console.error('❌ Error en fetchWeatherData:', error);
        throw error;
    }
}

function generateLocationWeatherData(location) {
    const coordinates = getCityCoordinates(location);
    const baseTemp = getBaseTemperatureForLocation(location);
    const weatherType = getWeatherTypeForLocation(location);
    
    return {
        name: location,
        lat: coordinates.lat,
        lng: coordinates.lng,
        temp: baseTemp,
        description: weatherType,
        humidity: Math.floor(Math.random() * 30) + 50,
        wind: Math.floor(Math.random() * 15) + 5,
        uv: Math.floor(Math.random() * 6) + 3,
        visibility: Math.floor(Math.random() * 10) + 5,
        pressure: Math.floor(Math.random() * 50) + 1000,
        feelsLike: baseTemp + Math.floor(Math.random() * 3) - 1
    };
}

function getCityCoordinates(cityName) {
    const cities = {
        'Madrid': { lat: 40.4168, lng: -3.7038 },
        'Barcelona': { lat: 41.3851, lng: 2.1734 },
        'Valencia': { lat: 39.4699, lng: -0.3763 },
        'Sevilla': { lat: 37.3891, lng: -5.9845 },
        'Zaragoza': { lat: 41.6488, lng: -0.8891 },
        'Málaga': { lat: 36.7213, lng: -4.4214 },
        'Murcia': { lat: 37.9922, lng: -1.1307 },
        'Palma': { lat: 39.5696, lng: 2.6502 },
        'Las Palmas': { lat: 28.1248, lng: -15.4300 },
        'Bilbao': { lat: 43.2627, lng: -2.9253 },
        'Alicante': { lat: 38.3452, lng: -0.4810 },
        'Córdoba': { lat: 37.8882, lng: -4.7794 },
        'Valladolid': { lat: 41.6523, lng: -4.7245 },
        'Vigo': { lat: 42.2406, lng: -8.7207 },
        'Gijón': { lat: 43.5453, lng: -5.6619 },
        'Hospitalet': { lat: 41.3596, lng: 2.0998 },
        'A Coruña': { lat: 43.3623, lng: -8.4115 },
        'Vitoria': { lat: 42.8467, lng: -2.6716 },
        'Granada': { lat: 37.1773, lng: -3.5986 },
        'Elche': { lat: 38.2622, lng: -0.7011 }
    };
    
    return cities[cityName] || { lat: 40.4168, lng: -3.7038 };
}

function getBaseTemperatureForLocation(location) {
    // Simulate different base temperatures for different cities
    const tempRanges = {
        'Madrid': [15, 25],
        'Barcelona': [18, 28],
        'Valencia': [20, 30],
        'Sevilla': [22, 32],
        'Málaga': [20, 30],
        'Murcia': [21, 31],
        'Palma': [19, 29],
        'Las Palmas': [22, 28],
        'Bilbao': [16, 24],
        'Vigo': [15, 23],
        'Gijón': [14, 22],
        'A Coruña': [14, 22],
        'Vitoria': [12, 20],
        'Granada': [18, 28],
        'Alicante': [19, 29]
    };
    
    const range = tempRanges[location] || [15, 25];
    return Math.floor(Math.random() * (range[1] - range[0] + 1)) + range[0];
}

function getWeatherTypeForLocation(location) {
    const weatherTypes = ['Soleado', 'Parcialmente nublado', 'Nublado', 'Lluvia ligera', 'Lluvia moderada', 'Nublado', 'Soleado'];
    return weatherTypes[Math.floor(Math.random() * weatherTypes.length)];
}

function updateMainWeatherFromMap(data) {
    // Add loading animation
    addLoadingEffect();
    
    // Load static past hours data from localStorage
    loadStaticPastHoursData();
    console.log('📂 Datos estáticos de horas pasadas cargados para mantener consistencia');
    
    // Update hourly forecast first to get current hour data
    updateHourlyForecast(data);
    
    // Get current hour temperature from hourly forecast for consistency
    const currentHour = new Date().getHours();
    let currentHourTemp = data.temp; // Fallback to original temp
    
    if (window.hourlyData && window.hourlyData.length > 0) {
        const currentHourData = window.hourlyData.find(h => h.hour === currentHour);
        if (currentHourData) {
            currentHourTemp = currentHourData.temp;
            console.log(`🌡️ Usando temperatura de hora actual (${currentHour}:00): ${currentHourTemp}°C`);
        }
    }
    
    // Update temperature with current hour temperature for consistency
    updateTemperature(currentHourTemp);
    
    // Update weather description
    updateWeatherDescription(data.description);
    
    // Update location in header
    updateLocation(data.name);
    
    // Update main weather location display
    updateMainWeatherLocation(data.name);
    
    // Update all weather details
    updateAllWeatherDetails(data);
    
    // Update weather icon based on description
    updateWeatherIcon(data.description);
    
    // Update weekly forecast with new data
    updateWeeklyForecast(data);
    
    // Update radar data for the new location
    updateRadarForLocation(data);
    
    // Update location coordinates display with exact location name
    updateLocationCoordinates(data);
    
    // Update weather alerts for current location
    updateWeatherAlerts(data);
    
    // Remove loading effect after a short delay
    setTimeout(() => {
        removeLoadingEffect();
    }, 1000);
}

function updateLocationCoordinates(data) {
    // Update the coordinates display with exact location name
    const coordinatesElements = document.querySelectorAll('.coordinates');
    
    coordinatesElements.forEach(element => {
        // Update coordinates (keep the original format)
        element.innerHTML = `Ubicación (${data.lat.toFixed(4)}, ${data.lng.toFixed(4)})`;
        
        // Add exact location name below coordinates
        const locationName = document.createElement('div');
        locationName.className = 'exact-location';
        locationName.style.cssText = `
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 5px;
            font-weight: 500;
            text-align: center;
        `;
        locationName.textContent = data.name;
        
        // Remove existing location name if any
        const existingLocation = element.querySelector('.exact-location');
        if (existingLocation) {
            existingLocation.remove();
        }
        
        // Add new location name
        element.appendChild(locationName);
    });
}

function updateWeatherAlerts(data) {
    console.log('⚠️ Actualizando alertas para:', data.name);
    
    const alertBanner = document.querySelector('.alert-banner');
    if (!alertBanner) return;
    
    // Generate alerts based on current weather data
    const alerts = generateLocationAlerts(data);
    
    if (alerts.length > 0) {
        // Show the first alert
        const alert = alerts[0];
        alertBanner.innerHTML = `
            <i class="${alert.icon}"></i>
            <span>${alert.title} - ${data.name}</span>
        `;
        alertBanner.className = `alert-banner ${alert.type}`;
        alertBanner.style.display = 'block';
        
        console.log('⚠️ Alerta mostrada:', alert.title);
    } else {
        // Hide alert banner if no alerts
        alertBanner.style.display = 'none';
        console.log('✅ Sin alertas para', data.name);
    }
}

function generateLocationAlerts(data) {
    const alerts = [];
    
    // Check for extreme temperatures
    if (data.temp > 35) {
        alerts.push({
            type: 'danger',
            icon: 'fas fa-thermometer-full',
            title: 'Ola de Calor',
            message: `Temperatura extrema de ${data.temp}°C en ${data.name}. Tome precauciones.`
        });
    }
    
    if (data.temp < -5) {
        alerts.push({
            type: 'warning',
            icon: 'fas fa-thermometer-empty',
            title: 'Ola de Frío',
            message: `Temperatura muy baja de ${data.temp}°C en ${data.name}. Abríguese bien.`
        });
    }
    
    // Check for high winds
    if (data.wind > 30) {
        alerts.push({
            type: 'warning',
            icon: 'fas fa-wind',
            title: 'Vientos Fuertes',
            message: `Vientos fuertes de ${data.wind} km/h en ${data.name}. Cuidado con objetos sueltos.`
        });
    }
    
    // Check for heavy rain
    if (data.description.includes('Lluvia') && data.description.includes('intensa')) {
        alerts.push({
            type: 'danger',
            icon: 'fas fa-cloud-rain',
            title: 'Lluvia Intensa',
            message: `Lluvia intensa en ${data.name}. Riesgo de inundaciones.`
        });
    }
    
    // Check for storms
    if (data.description.includes('Tormenta') || data.description.includes('tormenta')) {
        alerts.push({
            type: 'danger',
            icon: 'fas fa-bolt',
            title: 'Tormenta Eléctrica',
            message: `Tormenta eléctrica en ${data.name}. Evite actividades al aire libre.`
        });
    }
    
    return alerts;
}

function updateRadarForLocation(data) {
    // Update radar center to the new location
    const centerLat = data.lat;
    const centerLng = data.lng;
    
    // Regenerate radar data for the new location
    radarData = [];
    const radius = 2; // 2 degrees radius
    
    for (let i = 0; i < 50; i++) {
        const angle = (Math.PI * 2 * i) / 50;
        const distance = Math.random() * radius;
        const lat = centerLat + Math.cos(angle) * distance;
        const lng = centerLng + Math.sin(angle) * distance;
        
        // Generate precipitation intensity (0-30 mm/h)
        const intensity = Math.random() * 30;
        let color = '#00ff00'; // Light green
        
        if (intensity > 25) color = '#ff0000'; // Red
        else if (intensity > 10) color = '#ff8000'; // Orange
        else if (intensity > 2) color = '#ffff00'; // Yellow
        
        radarData.push({
            lat: lat,
            lng: lng,
            intensity: intensity,
            color: color,
            size: Math.max(3, intensity / 3)
        });
    }
    
    // Update radar display
    updateRadarDisplay();
}

function addLoadingEffect() {
    const elements = document.querySelectorAll('.temp-value, .temp-value-desktop, .weather-description, .weather-description-desktop');
    elements.forEach(el => {
        el.style.opacity = '0.6';
        el.style.animation = 'dataLoading 1s ease-in-out infinite alternate';
    });
}

function removeLoadingEffect() {
    const elements = document.querySelectorAll('.temp-value, .temp-value-desktop, .weather-description, .weather-description-desktop');
    elements.forEach(el => {
        el.style.opacity = '1';
        el.style.animation = 'none';
    });
}

function updateTemperature(temp) {
    const tempElements = document.querySelectorAll('.temp-value, .temp-value-desktop');
    tempElements.forEach(el => {
        el.style.animation = 'temperatureChange 0.5s ease-in-out';
        setTimeout(() => {
            el.textContent = temp + '°C';
            el.style.color = getTemperatureColor(temp);
        }, 250);
    });
}

function getTemperatureColor(temp) {
    if (temp < 10) return '#64b5f6'; // Blue
    if (temp < 20) return '#4caf50'; // Green
    if (temp < 30) return '#ffeb3b'; // Yellow
    return '#ff5722'; // Red
}

function updateWeatherDescription(description) {
    const descElements = document.querySelectorAll('.weather-description, .weather-description-desktop');
    descElements.forEach(el => {
        el.style.animation = 'dataUpdate 0.5s ease-in-out';
        setTimeout(() => {
            el.textContent = description;
        }, 250);
    });
}

function updateLocation(locationName) {
    const locationElements = document.querySelectorAll('.location-info span');
    locationElements.forEach(el => {
        el.style.animation = 'dataUpdate 0.5s ease-in-out';
        setTimeout(() => {
            el.textContent = locationName;
        }, 250);
    });
    
    // Add location indicator
    addLocationIndicator(locationName);
}

function addLocationIndicator(locationName) {
    // Remove existing indicator
    const existingIndicator = document.querySelector('.location-indicator');
    if (existingIndicator) {
        existingIndicator.remove();
    }
    
    // Create location indicator
    const indicator = document.createElement('div');
    indicator.className = 'location-indicator';
    indicator.innerHTML = `
        <i class="fas fa-map-marker-alt"></i>
        <span>${locationName}</span>
    `;
    
    // Add styles
    indicator.style.cssText = `
        position: fixed;
        top: 80px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(76, 175, 80, 0.9);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        animation: locationIndicatorSlide 0.5s ease-out;
    `;
    
    document.body.appendChild(indicator);
    
    // Remove indicator after 3 seconds
    setTimeout(() => {
        if (indicator.parentNode) {
            indicator.style.animation = 'locationIndicatorFadeOut 0.5s ease-in';
            setTimeout(() => {
                if (indicator.parentNode) {
                    indicator.parentNode.removeChild(indicator);
                }
            }, 500);
        }
    }, 3000);
}

function updateAllWeatherDetails(data) {
    const details = [
        { selector: '.detail-item:nth-child(1) .detail-value, .detail-item-desktop:nth-child(1) .detail-value', value: data.wind + ' km/h' },
        { selector: '.detail-item:nth-child(2) .detail-value, .detail-item-desktop:nth-child(2) .detail-value', value: data.humidity + '%' },
        { selector: '.detail-item:nth-child(3) .detail-value, .detail-item-desktop:nth-child(3) .detail-value', value: data.uv },
        { selector: '.detail-item:nth-child(4) .detail-value, .detail-item-desktop:nth-child(4) .detail-value', value: data.visibility + ' km' },
        { selector: '.detail-item:nth-child(5) .detail-value, .detail-item-desktop:nth-child(5) .detail-value', value: data.feelsLike + '°C' },
        { selector: '.detail-item:nth-child(6) .detail-value, .detail-item-desktop:nth-child(6) .detail-value', value: data.pressure + ' hPa' }
    ];
    
    details.forEach(detail => {
        const elements = document.querySelectorAll(detail.selector);
        elements.forEach(el => {
            el.style.animation = 'dataUpdate 0.5s ease-in-out';
            setTimeout(() => {
                el.textContent = detail.value;
            }, 250);
        });
    });
}

function updateWeatherIcon(description) {
    const iconMap = {
        'Soleado': 'fas fa-sun',
        'Parcialmente nublado': 'fas fa-cloud-sun',
        'Nublado': 'fas fa-cloud',
        'Lluvia ligera': 'fas fa-cloud-rain',
        'Lluvia moderada': 'fas fa-cloud-rain',
        'Lluvia intensa': 'fas fa-cloud-showers-heavy',
        'Tormenta': 'fas fa-bolt',
        'Nieve': 'fas fa-snowflake',
        'Niebla': 'fas fa-smog'
    };
    
    const iconClass = iconMap[description] || 'fas fa-sun';
    const iconElements = document.querySelectorAll('.weather-icon i, .weather-icon-desktop i');
    
    iconElements.forEach(icon => {
        icon.style.animation = 'dataUpdate 0.5s ease-in-out';
        setTimeout(() => {
            icon.className = iconClass;
        }, 250);
    });
}

function updateHourlyForecast(data) {
    console.log('🕐 Generando pronóstico de 24 horas...');
    
    // Get current time
    const now = new Date();
    const currentHour = now.getHours();
    
    // Check if we need to update only future hours (preserve past hours)
    if (window.hourlyData && window.hourlyData.length > 0) {
        const lastUpdateHour = window.hourlyData.find(h => h.isCurrent)?.hour;
        if (lastUpdateHour !== undefined && lastUpdateHour === currentHour) {
            console.log('⏰ Misma hora, actualizando solo horas futuras');
            updateFutureHoursOnly(data, currentHour);
            return;
        }
    }
    
    // Generate 24 hours of data (12 hours back + 12 hours forward from current hour)
    const hourlyData = generate24HourForecast(data, currentHour);
    
    // Find and set current hour index
    currentHourlyIndex = hourlyData.findIndex(h => h.isCurrent);
    if (currentHourlyIndex === -1) currentHourlyIndex = 0;
    
    console.log('📍 Índice de hora actual:', currentHourlyIndex);
    
    // Update mobile hourly forecast
    updateHourlyForecastMobile(hourlyData);
    
    // Update desktop hourly forecast
    updateHourlyForecastDesktop(hourlyData);
    
    // Update navigation buttons
    updateNavigationButtons();
    
    console.log('✅ Pronóstico de 24 horas generado');
}

function updateFutureHoursOnly(data, currentHour) {
    if (!window.hourlyData) return;
    
    console.log('🔄 Actualizando solo horas futuras...');
    
    // Update only future hours (current hour and beyond)
    window.hourlyData.forEach((hourData, index) => {
        if (!hourData.isPast) {
            // Update current and future hours with new data
            const baseTemp = data.temp;
            const baseDescription = data.description;
            
            let tempVariation = 0;
            if (hourData.hour >= 6 && hourData.hour <= 18) {
                tempVariation = Math.sin((hourData.hour - 6) * Math.PI / 12) * 5;
            } else {
                tempVariation = -3 - Math.random() * 3;
            }
            
            tempVariation += (Math.random() - 0.5) * 4;
            hourData.temp = Math.round(baseTemp + tempVariation);
            hourData.weather = generateWeatherForHour(hourData.hour, baseDescription);
            hourData.precipitation = calculatePrecipitationProbability(hourData.hour, baseDescription);
            
            // Update isCurrent status
            hourData.isCurrent = (hourData.hour === currentHour);
        }
    });
    
    // Update displays
    updateHourlyForecastMobile(window.hourlyData);
    updateHourlyForecastDesktop(window.hourlyData);
    updateNavigationButtons();
    
    console.log('✅ Horas futuras actualizadas');
}


function loadStaticPastHoursData() {
    const saved = localStorage.getItem('staticPastHoursData');
    if (saved) {
        try {
            staticPastHoursData = JSON.parse(saved);
            console.log('📂 Datos estáticos de horas pasadas cargados desde localStorage');
            console.log('📊 Datos cargados:', Object.keys(staticPastHoursData).length, 'horas');

            // Limpia datos de días anteriores
            cleanOldStaticData();
        } catch (error) {
            console.error('❌ Error cargando datos estáticos:', error);
            staticPastHoursData = {};
        }
    } else {
        console.log('📂 No hay datos estáticos guardados, se generarán nuevos');
        staticPastHoursData = {};
    }
}

function saveStaticPastHoursData() {
    try {
        localStorage.setItem('staticPastHoursData', JSON.stringify(staticPastHoursData));
        console.log('💾 Datos estáticos de horas pasadas guardados');
    } catch (error) {
        console.error('❌ Error guardando datos estáticos:', error);
    }
}

// Debug function to check static data
function debugStaticData() {
    console.log('🔍 DEBUG - Datos estáticos actuales:');
    console.log('📊 Total de horas guardadas:', Object.keys(staticPastHoursData).length);
    Object.keys(staticPastHoursData).forEach(hourKey => {
        const data = staticPastHoursData[hourKey];
        console.log(`  ${hourKey}: ${data.temp}°C ${data.weather} (${Math.round(data.precipitation * 100)}%)`);
    });
}

// Clean old static data (older than 24 hours)
function cleanOldStaticData() {
    const today = new Date().toDateString();
    const lastSavedDate = localStorage.getItem('staticDataDate');

    if (lastSavedDate !== today) {
        console.log('🧹 Limpiando datos estáticos antiguos...');
        localStorage.removeItem('staticPastHoursData');
        localStorage.setItem('staticDataDate', today);
        staticPastHoursData = {};
    }
}

function generate24HourForecast(data, currentHour) {
    const hourlyData = [];
    const baseTemp = data.temp;
    const baseDescription = data.description;
    
    console.log('🕐 Generando pronóstico de 24 horas para hora actual:', currentHour);
    console.log('📂 Datos estáticos disponibles:', Object.keys(staticPastHoursData));
    
    // Generate data for 24 hours (0-23)
    for (let hour = 0; hour < 24; hour++) {
        const date = new Date();
        date.setHours(hour, 0, 0, 0);
        
        let temp, weatherType, precipitationProb, icon;
        
        // 🔒 Si es una hora pasada, usamos los datos guardados
        if (hour < currentHour) {
            if (!staticPastHoursData[hour]) {
                // Si no hay guardado, lo generamos y guardamos la primera vez
                temp = Math.round(baseTemp + (Math.random() * 6 - 3));
                weatherType = generateWeatherForHour(hour, baseDescription);
                precipitationProb = calculatePrecipitationProbability(hour, baseDescription);
                icon = getWeatherIconForHour(weatherType, hour);
                
                staticPastHoursData[hour] = {
                    temp: temp,
                    weather: weatherType,
                    precipitation: precipitationProb,
                    icon: icon
                };
                saveStaticPastHoursData();
                console.log(`💾 Nuevos datos estáticos generados para ${hour}:00: ${temp}°C ${weatherType}`);
            } else {
                // Usar datos estáticos existentes
                temp = staticPastHoursData[hour].temp;
                weatherType = staticPastHoursData[hour].weather;
                precipitationProb = staticPastHoursData[hour].precipitation;
                icon = staticPastHoursData[hour].icon;
                console.log(`📂 Usando datos estáticos para ${hour}:00: ${temp}°C ${weatherType}`);
            }
        } else {
            // 🔄 Si es actual o futura, genera normalmente
            let tempVariation = 0;
            if (hour >= 6 && hour <= 18) {
                // Daytime: warmer
                tempVariation = Math.sin((hour - 6) * Math.PI / 12) * 5;
            } else {
                // Nighttime: cooler
                tempVariation = -3 - Math.random() * 3;
            }
            
            // Add some randomness
            tempVariation += (Math.random() - 0.5) * 4;
            temp = Math.round(baseTemp + tempVariation);
            weatherType = generateWeatherForHour(hour, baseDescription);
            precipitationProb = calculatePrecipitationProbability(hour, baseDescription);
            icon = getWeatherIconForHour(weatherType, hour);
            
            console.log(`🔄 Datos dinámicos para ${hour}:00: ${temp}°C ${weatherType}`);
        }
        
        hourlyData.push({
            hour: hour,
            time: formatHour(hour),
            temp: temp,
            weather: weatherType,
            precipitation: precipitationProb,
            icon: icon,
            isPast: hour < currentHour,
            isCurrent: hour === currentHour,
            date: date,
            index: hour
        });
    }
    
    console.log('🕐 Datos de 24 horas generados:', hourlyData.map(h => `${h.time}(${h.isPast ? 'P' : h.isCurrent ? 'C' : 'F'})`).join(' '));
    
    // Debug static data
    debugStaticData();
    
    return hourlyData;
}

function generateWeatherForHour(hour, baseWeather) {
    const weatherTypes = {
        'Soleado': ['Soleado', 'Parcialmente nublado', 'Soleado', 'Soleado'],
        'Parcialmente nublado': ['Parcialmente nublado', 'Nublado', 'Soleado', 'Parcialmente nublado'],
        'Nublado': ['Nublado', 'Lluvia ligera', 'Parcialmente nublado', 'Nublado'],
        'Lluvia ligera': ['Lluvia ligera', 'Lluvia moderada', 'Nublado', 'Lluvia ligera'],
        'Lluvia moderada': ['Lluvia moderada', 'Lluvia intensa', 'Lluvia ligera', 'Nublado']
    };
    
    const baseTypes = weatherTypes[baseWeather] || weatherTypes['Soleado'];
    
    // Night hours tend to be clearer
    if (hour >= 22 || hour <= 5) {
        return Math.random() < 0.7 ? 'Despejado' : baseTypes[Math.floor(Math.random() * baseTypes.length)];
    }
    
    // Day hours follow base weather pattern
    return baseTypes[Math.floor(Math.random() * baseTypes.length)];
}

function calculatePrecipitationProbability(hour, baseWeather) {
    const baseProb = {
        'Soleado': 0.1,
        'Parcialmente nublado': 0.2,
        'Nublado': 0.4,
        'Lluvia ligera': 0.6,
        'Lluvia moderada': 0.8
    };
    
    let prob = baseProb[baseWeather] || 0.3;
    
    // Higher probability during afternoon hours
    if (hour >= 14 && hour <= 18) {
        prob += 0.2;
    }
    
    // Lower probability during night
    if (hour >= 22 || hour <= 6) {
        prob -= 0.1;
    }
    
    return Math.max(0, Math.min(1, prob));
}

function formatHour(hour) {
    return hour.toString().padStart(2, '0') + ':00';
}

// Global variables for hourly navigation
let currentHourlyIndex = 0;
let hourlyData = [];
const HOURS_PER_VIEW = 6; // Show 6 hours at a time

function updateHourlyForecastMobile(hourlyData) {
    const hourlyContainer = document.querySelector('#hourly-list');
    if (!hourlyContainer) return;
    
    // Store data globally
    window.hourlyData = hourlyData;
    
    // Clear existing content
    hourlyContainer.innerHTML = '';
    
    // Show 6 hours starting from current index
    const startIndex = Math.max(0, currentHourlyIndex);
    const endIndex = Math.min(hourlyData.length, startIndex + HOURS_PER_VIEW);
    
    console.log('📱 Actualizando móvil:', {
        currentIndex: currentHourlyIndex,
        startIndex,
        endIndex,
        totalHours: hourlyData.length
    });
    
    for (let i = startIndex; i < endIndex; i++) {
        const hourData = hourlyData[i];
        const hourItem = document.createElement('div');
        hourItem.className = `hour-item ${hourData.isPast ? 'past-hour' : ''} ${hourData.isCurrent ? 'current-hour' : ''}`;
        
        hourItem.innerHTML = `
            <div class="hour-time">${hourData.time}</div>
            <div class="hour-icon">
                <i class="${getWeatherIconForHour(hourData.weather, hourData.hour)}"></i>
            </div>
            <div class="temp">${hourData.temp}°</div>
            <div class="hour-weather">${hourData.weather}</div>
            <div class="hour-precipitation">${Math.round(hourData.precipitation * 100)}%</div>
        `;
        
        hourlyContainer.appendChild(hourItem);
    }
    
    // Update navigation info
    updateHourlyNavigationInfo();
}

function updateHourlyForecastDesktop(hourlyData) {
    const hourlyContainer = document.querySelector('#hourly-list-desktop');
    if (!hourlyContainer) return;
    
    // Store data globally
    window.hourlyData = hourlyData;
    
    // Clear existing content
    hourlyContainer.innerHTML = '';
    
    // Show 6 hours starting from current index
    const startIndex = Math.max(0, currentHourlyIndex);
    const endIndex = Math.min(hourlyData.length, startIndex + HOURS_PER_VIEW);
    
    console.log('🖥️ Actualizando escritorio:', {
        currentIndex: currentHourlyIndex,
        startIndex,
        endIndex,
        totalHours: hourlyData.length
    });
    
    for (let i = startIndex; i < endIndex; i++) {
        const hourData = hourlyData[i];
        const hourItem = document.createElement('div');
        hourItem.className = `hour-item-desktop ${hourData.isPast ? 'past-hour' : ''} ${hourData.isCurrent ? 'current-hour' : ''}`;
        
        hourItem.innerHTML = `
            <div class="hour-time">${hourData.time}</div>
            <div class="hour-icon">
                <i class="${getWeatherIconForHour(hourData.weather, hourData.hour)}"></i>
            </div>
            <div class="temp">${hourData.temp}°</div>
            <div class="hour-weather">${hourData.weather}</div>
            <div class="hour-precipitation">${Math.round(hourData.precipitation * 100)}%</div>
        `;
        
        hourlyContainer.appendChild(hourItem);
    }
    
    // Update navigation info
    updateHourlyNavigationInfo();
}

function updateHourlyNavigationInfo() {
    const infoMobile = document.querySelector('#hourly-info');
    const infoDesktop = document.querySelector('#hourly-info-desktop');
    
    if (window.hourlyData && window.hourlyData.length > 0) {
        const startIndex = Math.max(0, currentHourlyIndex);
        const endIndex = Math.min(window.hourlyData.length, startIndex + HOURS_PER_VIEW);
        
        const startHour = window.hourlyData[startIndex]?.time || '00:00';
        const endHour = window.hourlyData[endIndex - 1]?.time || '23:00';
        
        const infoText = `${startHour} - ${endHour}`;
        
        if (infoMobile) infoMobile.textContent = infoText;
        if (infoDesktop) infoDesktop.textContent = infoText;
        
        console.log('📊 Info de navegación actualizada:', infoText);
    }
}

function navigateHourly(direction) {
    console.log('🔄 Navegando:', direction);
    
    if (!window.hourlyData || window.hourlyData.length === 0) {
        console.log('❌ No hay datos de horas disponibles');
        return;
    }
    
    const newIndex = currentHourlyIndex + direction;
    
    // Check bounds - allow navigation within the 24 hours
    if (newIndex < 0 || newIndex >= window.hourlyData.length) {
        console.log('❌ Límite alcanzado:', newIndex);
        return;
    }
    
    console.log('📍 Cambiando de índice', currentHourlyIndex, 'a', newIndex);
    currentHourlyIndex = newIndex;
    
    // Update both mobile and desktop
    updateHourlyForecastMobile(window.hourlyData);
    updateHourlyForecastDesktop(window.hourlyData);
    
    // Update navigation buttons
    updateNavigationButtons();
    
    console.log('✅ Navegación completada');
}

function updateNavigationButtons() {
    const prevMobile = document.querySelector('#hourly-prev');
    const nextMobile = document.querySelector('#hourly-next');
    const prevDesktop = document.querySelector('#hourly-prev-desktop');
    const nextDesktop = document.querySelector('#hourly-next-desktop');
    
    if (!window.hourlyData) return;
    
    // Allow navigation through all 24 hours
    const canGoPrev = currentHourlyIndex > 0;
    const canGoNext = currentHourlyIndex < window.hourlyData.length - 1;
    
    console.log('🎮 Botones de navegación:', {
        currentIndex: currentHourlyIndex,
        totalHours: window.hourlyData.length,
        canGoPrev,
        canGoNext
    });
    
    if (prevMobile) {
        prevMobile.disabled = !canGoPrev;
        prevMobile.style.opacity = canGoPrev ? '1' : '0.3';
    }
    if (nextMobile) {
        nextMobile.disabled = !canGoNext;
        nextMobile.style.opacity = canGoNext ? '1' : '0.3';
    }
    if (prevDesktop) {
        prevDesktop.disabled = !canGoPrev;
        prevDesktop.style.opacity = canGoPrev ? '1' : '0.3';
    }
    if (nextDesktop) {
        nextDesktop.disabled = !canGoNext;
        nextDesktop.style.opacity = canGoNext ? '1' : '0.3';
    }
}

function getWeatherIconForHour(weatherType, hourIndex) {
    const iconMap = {
        'Soleado': 'fas fa-sun',
        'Parcialmente nublado': 'fas fa-cloud-sun',
        'Nublado': 'fas fa-cloud',
        'Lluvia ligera': 'fas fa-cloud-rain',
        'Lluvia moderada': 'fas fa-cloud-rain',
        'Lluvia intensa': 'fas fa-cloud-showers-heavy',
        'Despejado': 'fas fa-moon'
    };
    
    // Night hours (22:00 - 05:00) show moon for clear weather
    if ((hourIndex >= 22 || hourIndex <= 5) && (weatherType === 'Soleado' || weatherType === 'Despejado')) {
        return 'fas fa-moon';
    }
    
    return iconMap[weatherType] || 'fas fa-sun';
}

function updateWeeklyForecast(data) {
    const weeklyItems = document.querySelectorAll('.day-item, .day-item-desktop');
    const today = new Date();
    
    weeklyItems.forEach((item, index) => {
        // Calculate the date for this day (starting from today)
        const dayDate = new Date(today);
        dayDate.setDate(today.getDate() + index);
        
        // Generate weather data for this specific day
        const dayWeather = generateDayWeather(data, dayDate, index);
        
        // Update day name
        const dayNameElement = item.querySelector('.day-name');
        if (dayNameElement) {
            const dayNames = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
            const dayName = dayNames[dayDate.getDay()];
            dayNameElement.textContent = dayName;
        }
        
        // Update date
        const dateElement = item.querySelector('.day-date');
        if (dateElement) {
            const dayNumber = dayDate.getDate();
            const monthNames = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
            const monthName = monthNames[dayDate.getMonth()];
            dateElement.textContent = `${dayNumber} ${monthName}`;
        }
        
        // Update temperature
        const tempElement = item.querySelector('.day-temp');
        if (tempElement) {
            tempElement.style.animation = 'dataUpdate 0.5s ease-in-out';
            setTimeout(() => {
                tempElement.textContent = dayWeather.maxTemp + '° / ' + dayWeather.minTemp + '°';
            }, 250 + (index * 100));
        }
        
        // Update weather icon
        const iconElement = item.querySelector('i');
        if (iconElement) {
            iconElement.style.animation = 'dataUpdate 0.5s ease-in-out';
            setTimeout(() => {
                iconElement.className = getWeatherIconForDay(dayWeather.weatherType, index);
            }, 250 + (index * 100));
        }
        
        // Add visual indicator for today
        if (index === 0) {
            item.classList.add('today');
            item.style.border = '2px solid #64b5f6';
            item.style.background = 'rgba(100, 181, 246, 0.1)';
        } else {
            item.classList.remove('today');
            item.style.border = '';
            item.style.background = '';
        }
    });
}

function generateDayWeather(data, date, dayIndex) {
    const baseTemp = data.temp;
    const baseDescription = data.description;
    
    // Calculate temperature variation based on day and season
    const dayOfYear = Math.floor((date - new Date(date.getFullYear(), 0, 0)) / (1000 * 60 * 60 * 24));
    const seasonalVariation = Math.sin((dayOfYear / 365) * 2 * Math.PI) * 8; // Seasonal variation
    
    // Day-specific variation
    const dayVariation = Math.sin((dayIndex * Math.PI) / 7) * 4; // Weekly pattern
    
    // Random variation
    const randomVariation = (Math.random() - 0.5) * 6;
    
    const maxTemp = Math.round(baseTemp + seasonalVariation + dayVariation + randomVariation);
    const minTemp = maxTemp - Math.floor(Math.random() * 8) - 3;
    
    // Generate weather type based on temperature and season
    const weatherTypes = ['Soleado', 'Parcialmente nublado', 'Nublado', 'Lluvia ligera', 'Lluvia moderada'];
    let weatherType;
    
    if (maxTemp > 25) {
        weatherType = Math.random() > 0.3 ? 'Soleado' : 'Parcialmente nublado';
    } else if (maxTemp < 10) {
        weatherType = Math.random() > 0.4 ? 'Nublado' : 'Lluvia ligera';
    } else {
        weatherType = weatherTypes[Math.floor(Math.random() * weatherTypes.length)];
    }
    
    return {
        maxTemp: maxTemp,
        minTemp: minTemp,
        weatherType: weatherType
    };
}

function getWeatherIconForDay(weatherType, dayIndex) {
    const iconMap = {
        'Soleado': 'fas fa-sun',
        'Parcialmente nublado': 'fas fa-cloud-sun',
        'Nublado': 'fas fa-cloud',
        'Lluvia ligera': 'fas fa-cloud-rain',
        'Lluvia moderada': 'fas fa-cloud-showers-heavy'
    };
    
    return iconMap[weatherType] || 'fas fa-sun';
}

function updateMainWeatherFromHour(hourItem) {
    const temp = hourItem.querySelector('.temp').textContent;
    const icon = hourItem.querySelector('i').className;
    
    // Update main temperature
    const tempElements = document.querySelectorAll('.temp-value, .temp-value-desktop');
    tempElements.forEach(el => {
        el.style.animation = 'temperatureChange 0.5s ease-in-out';
        setTimeout(() => {
            el.textContent = temp;
        }, 250);
    });
    
    // Update main weather icon
    const iconElements = document.querySelectorAll('.weather-icon i, .weather-icon-desktop i');
    iconElements.forEach(el => {
        el.style.animation = 'dataUpdate 0.5s ease-in-out';
        setTimeout(() => {
            el.className = icon;
        }, 250);
    });
}

function centerMapOnCity(weatherData) {
    console.log('🗺️ Centrando mapas en:', weatherData.lat, weatherData.lng, 'para', weatherData.name);
    
    if (mobileMap) {
        console.log('📱 Centrando mapa móvil');
        mobileMap.setView([weatherData.lat, weatherData.lng], 10);
        addSearchResultMarker(mobileMap, weatherData.lat, weatherData.lng, weatherData.name, weatherData.temp, weatherData.description, weatherData.humidity, weatherData.wind);
    } else {
        console.log('⚠️ Mapa móvil no inicializado');
    }
    
    if (desktopMap) {
        console.log('🖥️ Centrando mapa escritorio');
        desktopMap.setView([weatherData.lat, weatherData.lng], 10);
        addSearchResultMarker(desktopMap, weatherData.lat, weatherData.lng, weatherData.name, weatherData.temp, weatherData.description, weatherData.humidity, weatherData.wind);
    } else {
        console.log('⚠️ Mapa escritorio no inicializado');
    }
}

function addSearchResultMarker(map, lat, lng, name, temp, description, humidity, wind) {
    // Remove existing search markers
    if (map.searchMarker) {
        map.removeLayer(map.searchMarker);
    }
    
    // Add new search marker
    map.searchMarker = L.marker([lat, lng], {
        icon: L.divIcon({
            className: 'custom-marker search-result',
            html: `<div style="
                background: #4caf50;
                border: 3px solid #2e7d32;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                box-shadow: 0 2px 10px rgba(76, 175, 80, 0.5);
                animation: pulse 2s infinite;
            "></div>`,
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        })
    }).addTo(map);
    
    map.searchMarker.bindPopup(`
        <div class="weather-popup">
            <h4>${name}</h4>
            <div class="temp">${temp}°C</div>
            <div class="description">${description}</div>
            <div class="details">
                <div>Humedad: ${humidity}%</div>
                <div>Viento: ${wind} km/h</div>
            </div>
        </div>
    `);
}

function startRealTimeUpdates() {
    // Simulate real-time weather updates every 2 minutes (120 seconds)
    setInterval(() => {
        console.log('🔄 Actualización automática cada 2 minutos...');
        
        // Update current location weather data
        if (currentLocation) {
            console.log('📍 Actualizando datos de ubicación actual:', currentLocation.name);
            updateMainWeatherFromMap(currentLocation);
        } else {
            // Try to get current location again
            loadCurrentLocationWeather();
        }
        
        // Show notification
        showNotification('🔄 Datos actualizados automáticamente', 'info');
    }, 120000); // 2 minutes = 120,000 milliseconds
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#4caf50' : type === 'error' ? '#f44336' : '#2196f3'};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 500;
        animation: notificationSlideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'notificationSlideOut 0.3s ease-in';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes dataLoading {
        0% { opacity: 0.6; }
        100% { opacity: 1; }
    }
    
    @keyframes temperatureChange {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    @keyframes dataUpdate {
        0% { opacity: 0.7; transform: translateY(5px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes notificationSlideIn {
        0% { transform: translateX(100%); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes notificationSlideOut {
        0% { transform: translateX(0); opacity: 1; }
        100% { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// ==================== MAP FUNCTIONS ====================

function initializeMaps() {
    // Initialize mobile map
    mobileMap = L.map('interactive-map').setView([40.4168, -3.7038], 6);
    setupMapLayers(mobileMap);
    setupMapEvents(mobileMap);
    addWeatherMarkers(mobileMap);
    
    // Initialize desktop map
    desktopMap = L.map('interactive-map-desktop').setView([40.4168, -3.7038], 6);
    setupMapLayers(desktopMap);
    setupMapEvents(desktopMap);
    addWeatherMarkers(desktopMap);
    
    // Add map control interactions
    addMapControlInteractions();
    
    // Get current location
    getCurrentLocation();
}

function setupMapLayers(map) {
    // Define tile layers
    const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: '© Esri'
    });
    
    const streetLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    });
    
    const darkLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '© CARTO'
    });
    
    // Store layers
    map.layers = {
        satellite: satelliteLayer,
        street: streetLayer,
        dark: darkLayer
    };
    
    // Add default layer
    satelliteLayer.addTo(map);
}

function setupMapEvents(map) {
    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;
        
        // Dispatch custom event for coordinate capture
        const event = new CustomEvent('mapClick', {
            detail: { lat, lng }
        });
        document.dispatchEvent(event);
        
        // Get weather for clicked location
        getWeatherForLocation(lat, lng, map);
        addTemporaryMarker(map, lat, lng);
    });
}

function addWeatherMarkers(map) {
    // No longer add predefined city markers
    // The map will only show markers for searched locations and current location
    console.log('🗺️ Mapa inicializado sin marcadores predeterminados');
}

function createCustomIcon(type) {
    const colors = {
        hot: '#ff5722',
        cold: '#2196f3',
        normal: '#4caf50',
        manual: '#9c27b0'
    };
    
    const color = colors[type] || colors.normal;
    
    return L.divIcon({
        className: 'custom-marker',
        html: `<div style="
            background: ${color};
            border: 2px solid white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        "></div>`,
        iconSize: [20, 20],
        iconAnchor: [10, 10]
    });
}

function createWeatherPopup(data) {
    return `
        <div class="weather-popup">
            <h4>${data.name}</h4>
            <div class="temp">${data.temp}°C</div>
            <div class="description">${data.description}</div>
            <div class="details">
                <div>Humedad: ${data.humidity}%</div>
                <div>Viento: ${data.wind} km/h</div>
            </div>
        </div>
    `;
}

function addTemporaryMarker(map, lat, lng) {
    // Remove existing temporary marker
    if (map.tempMarker) {
        map.removeLayer(map.tempMarker);
    }
    
    // Add temporary marker
    map.tempMarker = L.marker([lat, lng], {
        icon: L.divIcon({
            className: 'custom-marker temporary',
            html: `<div style="
                background: #ff9800;
                border: 2px solid white;
                border-radius: 50%;
                width: 25px;
                height: 25px;
                box-shadow: 0 2px 10px rgba(255, 152, 0, 0.5);
                animation: pulse 2s infinite;
            "></div>`,
            iconSize: [25, 25],
            iconAnchor: [12.5, 12.5]
        })
    }).addTo(map);
    
    // Remove temporary marker after 5 seconds
    setTimeout(() => {
        if (map.tempMarker) {
            map.removeLayer(map.tempMarker);
        }
    }, 5000);
}

async function getWeatherForLocation(lat, lng, map) {
    console.log('🗺️ Obteniendo datos para ubicación del mapa:', lat, lng);
    showNotification('🌍 Obteniendo datos de la ubicación seleccionada...', 'info');
    
    try {
        // Try to get real weather data for the clicked location
        console.log('🌐 Consultando API para coordenadas:', lat, lng);
        const weatherData = await fetchWeatherDataByCoordinates(lat, lng);
        console.log('✅ Datos obtenidos del mapa:', weatherData);
        
        // Update all weather displays with the clicked location data
        updateMainWeatherFromMap(weatherData);
        
        // Add marker for the clicked location
        addTemporaryMarker(map, lat, lng);
        
        showNotification(`✅ Datos de ${weatherData.name} cargados`, 'success');
        console.log('🎉 Datos del mapa cargados exitosamente');
        
    } catch (error) {
        console.error('❌ Error fetching weather for map location:', error);
        console.log('🔄 Usando datos simulados como fallback...');
        
        // Fallback to simulated data if API fails
        const weatherData = {
            name: `Ubicación (${lat.toFixed(4)}, ${lng.toFixed(4)})`,
            lat: lat,
            lng: lng,
            temp: Math.floor(Math.random() * 20) + 15,
            description: ['Soleado', 'Parcialmente nublado', 'Nublado', 'Lluvia ligera'][Math.floor(Math.random() * 4)],
            humidity: Math.floor(Math.random() * 30) + 50,
            wind: Math.floor(Math.random() * 15) + 5,
            uv: Math.floor(Math.random() * 6) + 3,
            visibility: Math.floor(Math.random() * 10) + 5,
            pressure: Math.floor(Math.random() * 50) + 1000,
            feelsLike: Math.floor(Math.random() * 20) + 15
        };
        
        updateMainWeatherFromMap(weatherData);
        addTemporaryMarker(map, lat, lng);
        showNotification('⚠️ Mostrando datos simulados para la ubicación seleccionada', 'warning');
    }
}

function addMapControlInteractions() {
    // Locate button
    const locateBtns = document.querySelectorAll('#locate-btn, #locate-btn-desktop');
    locateBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            getCurrentLocation();
        });
    });
    
    // Layer button
    const layerBtns = document.querySelectorAll('#layer-btn, #layer-btn-desktop');
    layerBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            toggleMapLayer();
        });
    });
}

async function loadCurrentLocationWeather() {
    console.log('🌍 Iniciando carga de ubicación actual...');
    showNotification('🌍 Obteniendo tu ubicación actual...', 'info');
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            async function(position) {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                console.log('📍 Coordenadas obtenidas:', lat, lng);
                
                try {
                    console.log('🌐 Obteniendo datos meteorológicos reales...');
                    // Try to get weather data for current location using reverse geocoding
                    const weatherData = await fetchWeatherDataByCoordinates(lat, lng);
                    console.log('✅ Datos meteorológicos reales obtenidos:', weatherData);
                    
                    // Update all weather displays with current location data
                    updateMainWeatherFromMap(weatherData);
                    
                    // Center both maps on current location
                    if (mobileMap) {
                        mobileMap.setView([lat, lng], 10);
                        addCurrentLocationMarker(mobileMap, lat, lng);
                    }
                    
                    if (desktopMap) {
                        desktopMap.setView([lat, lng], 10);
                        addCurrentLocationMarker(desktopMap, lat, lng);
                    }
                    
                    showNotification(`✅ Ubicación actual: ${weatherData.name}`, 'success');
                    console.log('🎉 Carga de ubicación actual completada exitosamente');
                } catch (error) {
                    console.error('❌ Error fetching weather for current location:', error);
                    showNotification('⚠️ Error al obtener datos de tu ubicación. Por favor, busca una ciudad manualmente.', 'warning');
                    // Don't load any default location
                }
            },
            function(error) {
                console.error('❌ Error getting location:', error);
                let errorMessage = '⚠️ No se pudo obtener la ubicación. ';
                
                switch(error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage += 'Por favor, permite el acceso a la ubicación en tu navegador.';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage += 'La ubicación no está disponible.';
                        break;
                    case error.TIMEOUT:
                        errorMessage += 'Tiempo de espera agotado. Intenta de nuevo.';
                        break;
                    default:
                        errorMessage += 'Error desconocido.';
                        break;
                }
                
                showNotification(errorMessage, 'warning');
                // Don't load any default location
            },
            {
                enableHighAccuracy: true,
                timeout: 15000, // Increased timeout
                maximumAge: 300000 // 5 minutes
            }
        );
    } else {
        console.log('⚠️ Geolocalización no soportada');
        showNotification('⚠️ Geolocalización no soportada en tu navegador. Por favor, busca una ciudad manualmente.', 'warning');
        // Don't load any default location
    }
}

async function loadDefaultLocation() {
    console.log('⚠️ No se pudo obtener la ubicación del usuario');
    showNotification('⚠️ No se pudo obtener tu ubicación. Por favor, permite el acceso a la ubicación o busca una ciudad manualmente.', 'warning');
    
    // Don't load any default location, just show the message
    // The user will need to either allow location access or search for a city
}

async function fetchWeatherDataByCoordinates(lat, lng) {
    console.log('🔑 API Key configurada:', API_KEY !== 'TU_API_KEY' ? 'Sí' : 'No');
    
    // Check if API key is configured
    if (API_KEY === 'TU_API_KEY') {
        throw new Error('API key not configured');
    }
    
    const url = `${API_BASE_URL}/weather?lat=${lat}&lon=${lng}&appid=${API_KEY}&units=metric&lang=es`;
    console.log('🌐 URL de la API (coordenadas):', url);
    
    try {
        const response = await fetch(url);
        console.log('📡 Respuesta de la API (coordenadas):', response.status, response.statusText);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            console.error('❌ Error de la API (coordenadas):', errorData);
            throw new Error(`HTTP error! status: ${response.status} - ${errorData.message || response.statusText}`);
        }
        
        const data = await response.json();
        console.log('📊 Datos de la API (coordenadas):', data);
        
        // Transform API data to our format
        const transformedData = {
            name: data.name + ', ' + data.sys.country,
            lat: data.coord.lat,
            lng: data.coord.lon,
            temp: Math.round(data.main.temp),
            description: data.weather[0].description,
            humidity: data.main.humidity,
            wind: Math.round(data.wind.speed * 3.6), // Convert m/s to km/h
            uv: 0, // UV index not available in current weather API
            visibility: Math.round(data.visibility / 1000), // Convert m to km
            pressure: data.main.pressure,
            feelsLike: Math.round(data.main.feels_like),
            country: data.sys.country,
            weatherIcon: data.weather[0].icon
        };
        
        console.log('✅ Datos transformados (coordenadas):', transformedData);
        return transformedData;
        
    } catch (error) {
        console.error('❌ Error en fetchWeatherDataByCoordinates:', error);
        throw error;
    }
}

function getCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                
                // Center both maps on current location
                if (mobileMap) {
                    mobileMap.setView([lat, lng], 10);
                    addCurrentLocationMarker(mobileMap, lat, lng);
                }
                
                if (desktopMap) {
                    desktopMap.setView([lat, lng], 10);
                    addCurrentLocationMarker(desktopMap, lat, lng);
                }
                
                showNotification('Ubicación actual encontrada', 'success');
            },
            function(error) {
                console.error('Error getting location:', error);
                showNotification('No se pudo obtener la ubicación', 'error');
            }
        );
    } else {
        showNotification('Geolocalización no soportada', 'error');
    }
}

function addCurrentLocationMarker(map, lat, lng) {
    // Remove existing current location marker
    if (map.currentLocationMarker) {
        map.removeLayer(map.currentLocationMarker);
    }
    
    // Add current location marker
    map.currentLocationMarker = L.marker([lat, lng], {
        icon: L.divIcon({
            className: 'custom-marker current-location',
            html: `<div style="
                background: #ffeb3b;
                border: 3px solid #ff9800;
                border-radius: 50%;
                width: 25px;
                height: 25px;
                box-shadow: 0 2px 10px rgba(255, 235, 59, 0.5);
                animation: pulse 2s infinite;
            "></div>`,
            iconSize: [25, 25],
            iconAnchor: [12.5, 12.5]
        })
    }).addTo(map);
    
    map.currentLocationMarker.bindPopup(`
        <div class="weather-popup">
            <h4>Mi Ubicación</h4>
            <div class="temp">${Math.floor(Math.random() * 20) + 15}°C</div>
            <div class="description">Ubicación actual</div>
        </div>
    `);
}

function toggleMapLayer() {
    const layers = ['satellite', 'street', 'dark'];
    const currentIndex = layers.indexOf(currentLayer);
    const nextIndex = (currentIndex + 1) % layers.length;
    currentLayer = layers[nextIndex];
    
    // Update both maps
    if (mobileMap) {
        updateMapLayer(mobileMap, currentLayer);
    }
    
    if (desktopMap) {
        updateMapLayer(desktopMap, currentLayer);
    }
    
    const layerNames = {
        satellite: 'Satélite',
        street: 'Calle',
        dark: 'Oscuro'
    };
    
    showNotification(`Capa cambiada a: ${layerNames[currentLayer]}`, 'info');
}

function updateMapLayer(map, layerType) {
    // Remove current layer
    map.eachLayer(function(layer) {
        if (layer instanceof L.TileLayer) {
            map.removeLayer(layer);
        }
    });
    
    // Add new layer
    map.layers[layerType].addTo(map);
}

// ==================== ENHANCED RADAR SYSTEM ====================

let radarAnimation = null;
let radarData = [];
let currentRadarTime = 0;

function initializeEnhancedRadar() {
    // Initialize radar data
    generateRadarData();
    
    // Setup radar controls
    setupRadarControls();
    
    // Start radar animation
    startRadarAnimation();
    
    // Update radar info
    updateRadarInfo();
}

function generateRadarData() {
    // Generate realistic radar precipitation data
    radarData = [];
    const centerLat = 40.4168; // Madrid
    const centerLng = -3.7038;
    const radius = 2; // 2 degrees radius
    
    for (let i = 0; i < 50; i++) {
        const angle = (Math.PI * 2 * i) / 50;
        const distance = Math.random() * radius;
        const lat = centerLat + Math.cos(angle) * distance;
        const lng = centerLng + Math.sin(angle) * distance;
        
        // Generate precipitation intensity (0-30 mm/h)
        const intensity = Math.random() * 30;
        let color = '#00ff00'; // Light green
        
        if (intensity > 25) color = '#ff0000'; // Red
        else if (intensity > 10) color = '#ff8000'; // Orange
        else if (intensity > 2) color = '#ffff00'; // Yellow
        
        radarData.push({
            lat: lat,
            lng: lng,
            intensity: intensity,
            color: color,
            size: Math.max(3, intensity / 3)
        });
    }
}

function setupRadarControls() {
    // Mobile radar controls
    const playBtn = document.getElementById('play-radar');
    const pauseBtn = document.getElementById('pause-radar');
    const refreshBtn = document.getElementById('refresh-radar');
    
    // Desktop radar controls
    const playBtnDesktop = document.getElementById('play-radar-desktop');
    const pauseBtnDesktop = document.getElementById('pause-radar-desktop');
    const refreshBtnDesktop = document.getElementById('refresh-radar-desktop');
    
    if (playBtn) {
        playBtn.addEventListener('click', () => {
            startRadarAnimation();
            playBtn.classList.add('active');
            pauseBtn.classList.remove('active');
        });
    }
    
    if (pauseBtn) {
        pauseBtn.addEventListener('click', () => {
            stopRadarAnimation();
            pauseBtn.classList.add('active');
            playBtn.classList.remove('active');
        });
    }
    
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            refreshRadarData();
        });
    }
    
    // Desktop controls
    if (playBtnDesktop) {
        playBtnDesktop.addEventListener('click', () => {
            startRadarAnimation();
            playBtnDesktop.classList.add('active');
            pauseBtnDesktop.classList.remove('active');
        });
    }
    
    if (pauseBtnDesktop) {
        pauseBtnDesktop.addEventListener('click', () => {
            stopRadarAnimation();
            pauseBtnDesktop.classList.add('active');
            playBtnDesktop.classList.remove('active');
        });
    }
    
    if (refreshBtnDesktop) {
        refreshBtnDesktop.addEventListener('click', () => {
            refreshRadarData();
        });
    }
}

function startRadarAnimation() {
    if (radarAnimation) return;
    
    radarAnimation = setInterval(() => {
        updateRadarDisplay();
        currentRadarTime = (currentRadarTime + 1) % 12; // 12 time steps
    }, 1000);
}

function stopRadarAnimation() {
    if (radarAnimation) {
        clearInterval(radarAnimation);
        radarAnimation = null;
    }
}

function updateRadarDisplay() {
    // Update radar sweep animation
    const radarMaps = document.querySelectorAll('.radar-map, .radar-map-desktop');
    radarMaps.forEach(map => {
        // Remove existing sweep
        const existingSweep = map.querySelector('.radar-sweep');
        if (existingSweep) {
            existingSweep.remove();
        }
        
        // Add new sweep
        const sweep = document.createElement('div');
        sweep.className = 'radar-sweep';
        map.appendChild(sweep);
        
        // Add precipitation dots
        radarData.forEach(point => {
            const dot = document.createElement('div');
            dot.style.position = 'absolute';
            dot.style.left = '50%';
            dot.style.top = '50%';
            dot.style.width = point.size + 'px';
            dot.style.height = point.size + 'px';
            dot.style.backgroundColor = point.color;
            dot.style.borderRadius = '50%';
            dot.style.transform = 'translate(-50%, -50%)';
            dot.style.opacity = '0.8';
            dot.style.boxShadow = `0 0 ${point.size * 2}px ${point.color}`;
            dot.style.animation = 'pulse 2s infinite';
            
            // Position based on lat/lng (simplified)
            const x = (point.lng + 3.7038) * 50 + 50;
            const y = (40.4168 - point.lat) * 50 + 50;
            dot.style.left = x + '%';
            dot.style.top = y + '%';
            
            map.appendChild(dot);
            
            // Remove dot after animation
            setTimeout(() => {
                if (dot.parentNode) {
                    dot.parentNode.removeChild(dot);
                }
            }, 2000);
        });
    });
    
    // Update radar info
    updateRadarInfo();
}

function updateRadarInfo() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('es-ES', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    // Update mobile radar info
    const radarTime = document.getElementById('radar-time');
    const radarRange = document.getElementById('radar-range');
    const radarPrecipitation = document.getElementById('radar-precipitation');
    
    if (radarTime) radarTime.textContent = timeString;
    if (radarRange) radarRange.textContent = '250 km';
    
    // Calculate average precipitation
    const avgPrecipitation = radarData.reduce((sum, point) => sum + point.intensity, 0) / radarData.length;
    if (radarPrecipitation) {
        radarPrecipitation.textContent = avgPrecipitation.toFixed(1) + ' mm/h';
    }
    
    // Update desktop radar info
    const radarTimeDesktop = document.getElementById('radar-time-desktop');
    const radarRangeDesktop = document.getElementById('radar-range-desktop');
    const radarPrecipitationDesktop = document.getElementById('radar-precipitation-desktop');
    
    if (radarTimeDesktop) radarTimeDesktop.textContent = timeString;
    if (radarRangeDesktop) radarRangeDesktop.textContent = '250 km';
    if (radarPrecipitationDesktop) {
        radarPrecipitationDesktop.textContent = avgPrecipitation.toFixed(1) + ' mm/h';
    }
}

function refreshRadarData() {
    // Regenerate radar data
    generateRadarData();
    
    // Update display
    updateRadarDisplay();
    
    // Show notification
    showNotification('Radar actualizado', 'success');
}

// ==================== WEATHER REPORT SYSTEM ====================

function addWeatherReportInteractions() {
    const modal = document.getElementById('weather-report-modal');
    const openBtn = document.getElementById('weather-report-btn');
    const closeBtn = document.getElementById('close-report-modal');
    const generateBtn = document.getElementById('generate-report');
    
    // Open modal
    openBtn.addEventListener('click', function() {
        modal.classList.add('active');
        updateReportLocation();
    });
    
    // Close modal
    closeBtn.addEventListener('click', closeReportModal);
    
    // Close modal when clicking outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeReportModal();
        }
    });
    
    // Generate report
    generateBtn.addEventListener('click', function() {
        generateWeatherReport();
    });
}

function closeReportModal() {
    const modal = document.getElementById('weather-report-modal');
    modal.classList.remove('active');
}

function updateReportLocation() {
    const locationInfo = document.querySelector('.location-info span');
    const reportLocation = document.getElementById('report-location');
    if (locationInfo && reportLocation) {
        // Extract city name from location string (remove country if present)
        const locationText = locationInfo.textContent;
        const cityName = locationText.includes(',') ? locationText.split(',')[0].trim() : locationText;
        reportLocation.value = cityName;
    }
}

async function generateWeatherReport() {
    const location = document.getElementById('report-location').value;
    const period = parseInt(document.getElementById('report-period').value);
    const type = document.getElementById('report-type').value;
    
    if (!location.trim()) {
        showNotification('Por favor ingrese una ubicación', 'error');
        return;
    }
    
    // Show loading
    showReportLoading();
    
    try {
        // Try to get real weather data first
        const currentWeather = await fetchWeatherData(location);
        const reportData = generateAdvancedWeatherReport(location, period, type, currentWeather);
        displayWeatherReport(reportData);
    } catch (error) {
        console.error('Error generating weather report:', error);
        // Fallback to simulated data
        const fallbackWeather = generateLocationWeatherData(location);
        const reportData = generateAdvancedWeatherReport(location, period, type, fallbackWeather);
        displayWeatherReport(reportData);
    }
}

function showReportLoading() {
    const content = document.getElementById('weather-report-content');
    content.innerHTML = `
        <div class="report-loading">
            <i class="fas fa-cloud-sun"></i>
            <h3>Generando Reporte Meteorológico</h3>
            <p>Analizando patrones climáticos y aplicando fórmulas meteorológicas...</p>
        </div>
    `;
}

function generateAdvancedWeatherReport(location, period, type, currentWeatherData = null) {
    const coordinates = currentWeatherData ? 
        { lat: currentWeatherData.lat, lng: currentWeatherData.lng } : 
        getCityCoordinates(location);
    
    const currentWeather = currentWeatherData || getCurrentWeatherData(location);
    
    // Generate forecast using meteorological formulas
    const forecast = generateMeteorologicalForecast(coordinates, currentWeather, period);
    
    // Calculate weather statistics
    const statistics = calculateWeatherStatistics(forecast);
    
    // Generate weather alerts
    const alerts = generateWeatherAlerts(forecast, currentWeather);
    
    // Generate charts data
    const chartsData = generateChartsData(forecast);
    
    return {
        location: location,
        coordinates: coordinates,
        currentWeather: currentWeather,
        forecast: forecast,
        statistics: statistics,
        alerts: alerts,
        chartsData: chartsData,
        generatedAt: new Date(),
        period: period,
        type: type
    };
}

function getCurrentWeatherData(location) {
    // Get current weather data for the location
    const coordinates = getCityCoordinates(location);
    const baseTemp = getBaseTemperatureForLocation(location);
    const weatherType = getWeatherTypeForLocation(location);
    
    return {
        name: location,
        lat: coordinates.lat,
        lng: coordinates.lng,
        temp: baseTemp,
        description: weatherType,
        humidity: Math.floor(Math.random() * 30) + 50,
        wind: Math.floor(Math.random() * 15) + 5,
        uv: Math.floor(Math.random() * 6) + 3,
        visibility: Math.floor(Math.random() * 10) + 5,
        pressure: Math.floor(Math.random() * 50) + 1000,
        feelsLike: baseTemp + Math.floor(Math.random() * 3) - 1
    };
}

function generateMeteorologicalForecast(coordinates, currentWeather, days) {
    const forecast = [];
    const baseTemp = currentWeather.temp;
    const baseHumidity = currentWeather.humidity;
    const basePressure = currentWeather.pressure;
    
    for (let i = 0; i < days; i++) {
        const date = new Date();
        date.setDate(date.getDate() + i);
        
        // Apply meteorological formulas for temperature prediction
        const tempVariation = calculateTemperatureVariation(coordinates, date, i);
        const temperature = Math.round(baseTemp + tempVariation);
        
        // Calculate humidity using dew point formula
        const humidity = calculateHumidityPrediction(baseHumidity, temperature, i);
        
        // Calculate pressure using barometric pressure formula
        const pressure = calculatePressurePrediction(basePressure, temperature, humidity, i);
        
        // Calculate wind using pressure gradient
        const wind = calculateWindPrediction(pressure, coordinates, i);
        
        // Calculate precipitation probability
        const precipitation = calculatePrecipitationProbability(humidity, pressure, temperature, i);
        
        // Determine weather type based on meteorological conditions
        const weatherType = determineWeatherType(temperature, humidity, precipitation, pressure);
        
        // Calculate UV index
        const uvIndex = calculateUVIndex(coordinates, date, temperature);
        
        // Calculate visibility
        const visibility = calculateVisibility(humidity, precipitation, wind);
        
        // Calculate heat index and wind chill
        const heatIndex = calculateHeatIndex(temperature, humidity);
        const windChill = calculateWindChill(temperature, wind);
        
        forecast.push({
            date: date,
            dayName: getDayName(date),
            temperature: temperature,
            minTemp: temperature - Math.floor(Math.random() * 8 + 3),
            maxTemp: temperature + Math.floor(Math.random() * 6 + 2),
            humidity: humidity,
            pressure: pressure,
            wind: wind,
            windDirection: getWindDirection(i),
            precipitation: precipitation,
            precipitationProbability: Math.round(precipitation * 100),
            weatherType: weatherType,
            uvIndex: uvIndex,
            visibility: visibility,
            heatIndex: heatIndex,
            windChill: windChill,
            description: getWeatherDescription(weatherType, temperature)
        });
    }
    
    return forecast;
}

// ==================== METEOROLOGICAL FORMULAS ====================

function calculateTemperatureVariation(coordinates, date, dayOffset) {
    // Temperature variation based on latitude, season, and day
    const lat = coordinates.lat;
    const month = date.getMonth();
    const dayOfYear = Math.floor((date - new Date(date.getFullYear(), 0, 0)) / 86400000);
    
    // Seasonal temperature variation (simplified)
    const seasonalVariation = Math.sin((dayOfYear - 80) * 2 * Math.PI / 365) * 15;
    
    // Latitude effect
    const latitudeEffect = (Math.abs(lat) - 40) * 0.5;
    
    // Daily random variation
    const dailyVariation = (Math.random() - 0.5) * 8;
    
    // Trend over time (gradual change)
    const trend = dayOffset * (Math.random() - 0.5) * 0.5;
    
    return seasonalVariation + latitudeEffect + dailyVariation + trend;
}

function calculateHumidityPrediction(baseHumidity, temperature, dayOffset) {
    // Humidity decreases with temperature increase (simplified)
    const tempEffect = (temperature - 20) * -0.5;
    
    // Seasonal variation
    const seasonalEffect = Math.sin(dayOffset * 0.1) * 10;
    
    // Random daily variation
    const dailyVariation = (Math.random() - 0.5) * 15;
    
    const humidity = baseHumidity + tempEffect + seasonalEffect + dailyVariation;
    
    return Math.max(20, Math.min(95, Math.round(humidity)));
}

function calculatePressurePrediction(basePressure, temperature, humidity, dayOffset) {
    // Pressure decreases with temperature increase
    const tempEffect = (temperature - 20) * -0.3;
    
    // Humidity effect on pressure
    const humidityEffect = (humidity - 50) * 0.1;
    
    // Cyclonic/anticyclonic patterns
    const pressurePattern = Math.sin(dayOffset * 0.2) * 5;
    
    // Random variation
    const randomVariation = (Math.random() - 0.5) * 10;
    
    const pressure = basePressure + tempEffect + humidityEffect + pressurePattern + randomVariation;
    
    return Math.max(980, Math.min(1040, Math.round(pressure)));
}

function calculateWindPrediction(pressure, coordinates, dayOffset) {
    // Wind speed based on pressure gradient (simplified)
    const pressureGradient = Math.abs(pressure - 1013) * 0.1;
    
    // Latitude effect (stronger winds at higher latitudes)
    const latitudeEffect = Math.abs(coordinates.lat) * 0.2;
    
    // Seasonal variation
    const seasonalEffect = Math.sin(dayOffset * 0.15) * 3;
    
    // Random variation
    const randomVariation = (Math.random() - 0.5) * 8;
    
    const wind = pressureGradient + latitudeEffect + seasonalEffect + randomVariation;
    
    return Math.max(0, Math.min(50, Math.round(wind)));
}

function calculatePrecipitationProbability(humidity, pressure, temperature, dayOffset) {
    // Higher humidity increases precipitation probability
    const humidityEffect = (humidity - 50) / 100;
    
    // Lower pressure increases precipitation probability
    const pressureEffect = (1013 - pressure) / 100;
    
    // Temperature effect (warmer air holds more moisture)
    const tempEffect = (temperature - 15) / 100;
    
    // Seasonal patterns
    const seasonalEffect = Math.sin(dayOffset * 0.3) * 0.2;
    
    const probability = humidityEffect + pressureEffect + tempEffect + seasonalEffect;
    
    return Math.max(0, Math.min(1, probability));
}

function determineWeatherType(temperature, humidity, precipitation, pressure) {
    const precipProb = precipitation;
    
    if (precipProb > 0.7) {
        if (temperature < 0) return 'Nieve';
        if (precipProb > 0.9) return 'Lluvia intensa';
        if (precipProb > 0.8) return 'Lluvia moderada';
        return 'Lluvia ligera';
    }
    
    if (pressure < 1000) return 'Tormenta';
    if (humidity > 80) return 'Niebla';
    if (humidity > 60) return 'Nublado';
    if (humidity > 40) return 'Parcialmente nublado';
    return 'Soleado';
}

function calculateUVIndex(coordinates, date, temperature) {
    // UV index based on latitude, season, and temperature
    const lat = Math.abs(coordinates.lat);
    const month = date.getMonth();
    
    // Maximum UV at equator, decreases with latitude
    const latitudeEffect = Math.cos(lat * Math.PI / 180) * 10;
    
    // Seasonal variation (higher in summer)
    const seasonalEffect = Math.sin((month - 5) * Math.PI / 6) * 3;
    
    // Temperature effect
    const tempEffect = (temperature - 20) * 0.1;
    
    const uvIndex = latitudeEffect + seasonalEffect + tempEffect;
    
    return Math.max(0, Math.min(11, Math.round(uvIndex)));
}

function calculateVisibility(humidity, precipitation, wind) {
    // Visibility decreases with humidity and precipitation
    const humidityEffect = (100 - humidity) * 0.1;
    const precipEffect = (1 - precipitation) * 10;
    const windEffect = wind * 0.2; // Wind can clear fog
    
    const visibility = humidityEffect + precipEffect + windEffect;
    
    return Math.max(1, Math.min(20, Math.round(visibility)));
}

function calculateHeatIndex(temperature, humidity) {
    // Heat index formula (simplified)
    if (temperature < 27) return temperature;
    
    const hi = -8.78469475556 + 1.61139411 * temperature + 2.33854883889 * humidity +
               -0.14611605 * temperature * humidity + -0.012308094 * Math.pow(temperature, 2) +
               -0.0164248277778 * Math.pow(humidity, 2) + 0.002211732 * Math.pow(temperature, 2) * humidity +
               0.00072546 * temperature * Math.pow(humidity, 2) - 0.000003582 * Math.pow(temperature, 2) * Math.pow(humidity, 2);
    
    return Math.round(hi);
}

function calculateWindChill(temperature, wind) {
    // Wind chill formula (simplified)
    if (temperature > 10) return temperature;
    
    const wc = 13.12 + 0.6215 * temperature - 11.37 * Math.pow(wind, 0.16) + 0.3965 * temperature * Math.pow(wind, 0.16);
    
    return Math.round(wc);
}

function getWindDirection(dayOffset) {
    const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
    return directions[dayOffset % directions.length];
}

function getWeatherDescription(weatherType, temperature) {
    const descriptions = {
        'Soleado': `Soleado y despejado`,
        'Parcialmente nublado': `Parcialmente nublado`,
        'Nublado': `Nublado`,
        'Lluvia ligera': `Lluvia ligera`,
        'Lluvia moderada': `Lluvia moderada`,
        'Lluvia intensa': `Lluvia intensa`,
        'Tormenta': `Tormenta eléctrica`,
        'Nieve': `Nieve`,
        'Niebla': `Niebla densa`
    };
    
    return descriptions[weatherType] || 'Condiciones variables';
}

function calculateWeatherStatistics(forecast) {
    const temps = forecast.map(day => day.temperature);
    const humidities = forecast.map(day => day.humidity);
    const pressures = forecast.map(day => day.pressure);
    const winds = forecast.map(day => day.wind);
    
    return {
        avgTemperature: Math.round(temps.reduce((a, b) => a + b, 0) / temps.length),
        minTemperature: Math.min(...temps),
        maxTemperature: Math.max(...temps),
        avgHumidity: Math.round(humidities.reduce((a, b) => a + b, 0) / humidities.length),
        avgPressure: Math.round(pressures.reduce((a, b) => a + b, 0) / pressures.length),
        avgWind: Math.round(winds.reduce((a, b) => a + b, 0) / winds.length),
        maxWind: Math.max(...winds),
        precipitationDays: forecast.filter(day => day.precipitation > 0.3).length,
        sunnyDays: forecast.filter(day => day.weatherType === 'Soleado').length
    };
}

function generateWeatherAlerts(forecast, currentWeather) {
    const alerts = [];
    
    // Check for extreme temperatures
    const maxTemp = Math.max(...forecast.map(day => day.maxTemp));
    const minTemp = Math.min(...forecast.map(day => day.minTemp));
    
    if (maxTemp > 35) {
        alerts.push({
            type: 'danger',
            icon: 'fas fa-thermometer-full',
            title: 'Ola de Calor',
            message: `Temperaturas extremas esperadas hasta ${maxTemp}°C. Tome precauciones.`
        });
    }
    
    if (minTemp < -5) {
        alerts.push({
            type: 'warning',
            icon: 'fas fa-thermometer-empty',
            title: 'Ola de Frío',
            message: `Temperaturas muy bajas esperadas hasta ${minTemp}°C. Abríguese bien.`
        });
    }
    
    // Check for heavy precipitation
    const heavyRainDays = forecast.filter(day => day.precipitation > 0.8).length;
    if (heavyRainDays > 2) {
        alerts.push({
            type: 'warning',
            icon: 'fas fa-cloud-rain',
            title: 'Lluvias Intensas',
            message: `${heavyRainDays} días de lluvia intensa esperados. Riesgo de inundaciones.`
        });
    }
    
    // Check for high winds
    const highWindDays = forecast.filter(day => day.wind > 30).length;
    if (highWindDays > 0) {
        alerts.push({
            type: 'warning',
            icon: 'fas fa-wind',
            title: 'Vientos Fuertes',
            message: `${highWindDays} días con vientos fuertes esperados. Cuidado con objetos sueltos.`
        });
    }
    
    // Check for storms
    const stormDays = forecast.filter(day => day.weatherType === 'Tormenta').length;
    if (stormDays > 0) {
        alerts.push({
            type: 'danger',
            icon: 'fas fa-bolt',
            title: 'Tormentas Eléctricas',
            message: `${stormDays} días con tormentas esperados. Evite actividades al aire libre.`
        });
    }
    
    return alerts;
}

function generateChartsData(forecast) {
    return {
        temperature: {
            labels: forecast.map(day => day.dayName),
            data: forecast.map(day => day.temperature),
            minData: forecast.map(day => day.minTemp),
            maxData: forecast.map(day => day.maxTemp)
        },
        humidity: {
            labels: forecast.map(day => day.dayName),
            data: forecast.map(day => day.humidity)
        },
        pressure: {
            labels: forecast.map(day => day.dayName),
            data: forecast.map(day => day.pressure)
        },
        wind: {
            labels: forecast.map(day => day.dayName),
            data: forecast.map(day => day.wind)
        },
        precipitation: {
            labels: forecast.map(day => day.dayName),
            data: forecast.map(day => day.precipitationProbability)
        }
    };
}

function displayWeatherReport(reportData) {
    const content = document.getElementById('weather-report-content');
    
    content.innerHTML = `
        <div class="weather-summary">
            <div class="summary-card">
                <h4>Temperatura Promedio</h4>
                <div class="value">${reportData.statistics.avgTemperature}°C</div>
                <div class="unit">Rango: ${reportData.statistics.minTemperature}° - ${reportData.statistics.maxTemperature}°</div>
            </div>
            <div class="summary-card">
                <h4>Humedad Promedio</h4>
                <div class="value">${reportData.statistics.avgHumidity}%</div>
                <div class="unit">Condiciones ${getHumidityDescription(reportData.statistics.avgHumidity)}</div>
            </div>
            <div class="summary-card">
                <h4>Presión Promedio</h4>
                <div class="value">${reportData.statistics.avgPressure} hPa</div>
                <div class="unit">${getPressureDescription(reportData.statistics.avgPressure)}</div>
            </div>
            <div class="summary-card">
                <h4>Viento Promedio</h4>
                <div class="value">${reportData.statistics.avgWind} km/h</div>
                <div class="unit">Máximo: ${reportData.statistics.maxWind} km/h</div>
            </div>
        </div>
        
        ${reportData.alerts.length > 0 ? `
        <div class="weather-alerts">
            <h3><i class="fas fa-exclamation-triangle"></i> Alertas Meteorológicas</h3>
            ${reportData.alerts.map(alert => `
                <div class="alert-item ${alert.type}">
                    <i class="alert-icon ${alert.icon}"></i>
                    <div class="alert-content">
                        <h5>${alert.title}</h5>
                        <p>${alert.message}</p>
                    </div>
                </div>
            `).join('')}
        </div>
        ` : ''}
        
        <div class="weather-charts">
            <div class="chart-container">
                <div class="chart-title">
                    <i class="fas fa-chart-line"></i>
                    Predicción de Temperaturas
                </div>
                <div class="chart-placeholder">
                    <i class="fas fa-chart-area"></i>
                    <p>Gráfico de temperaturas (máximas, mínimas y promedio)</p>
                </div>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">
                    <i class="fas fa-tint"></i>
                    Predicción de Precipitaciones
                </div>
                <div class="chart-placeholder">
                    <i class="fas fa-chart-bar"></i>
                    <p>Probabilidad de precipitaciones por día</p>
                </div>
            </div>
        </div>
        
        <div class="daily-forecast">
            <h3><i class="fas fa-calendar-alt"></i> Predicción Diaria</h3>
            <div class="forecast-grid">
                ${reportData.forecast.map(day => `
                    <div class="forecast-day">
                        <div class="forecast-day-header">
                            <div class="forecast-date">${day.dayName}</div>
                            <div class="forecast-temp">${day.temperature}°C</div>
                        </div>
                        <div class="forecast-details">
                            <div class="forecast-detail">
                                <div class="forecast-detail-label">Mín/Máx</div>
                                <div class="forecast-detail-value">${day.minTemp}°/${day.maxTemp}°</div>
                            </div>
                            <div class="forecast-detail">
                                <div class="forecast-detail-label">Humedad</div>
                                <div class="forecast-detail-value">${day.humidity}%</div>
                            </div>
                            <div class="forecast-detail">
                                <div class="forecast-detail-label">Viento</div>
                                <div class="forecast-detail-value">${day.wind} km/h</div>
                            </div>
                            <div class="forecast-detail">
                                <div class="forecast-detail-label">Precipitación</div>
                                <div class="forecast-detail-value">${day.precipitationProbability}%</div>
                            </div>
                            <div class="forecast-detail">
                                <div class="forecast-detail-label">UV</div>
                                <div class="forecast-detail-value">${day.uvIndex}</div>
                            </div>
                            <div class="forecast-detail">
                                <div class="forecast-detail-label">Visibilidad</div>
                                <div class="forecast-detail-value">${day.visibility} km</div>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
        
        <div class="weather-stats">
            <div class="stat-item">
                <div class="stat-value">${reportData.statistics.sunnyDays}</div>
                <div class="stat-label">Días Soleados</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">${reportData.statistics.precipitationDays}</div>
                <div class="stat-label">Días de Lluvia</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">${reportData.forecast.length}</div>
                <div class="stat-label">Días Analizados</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">${Math.round((reportData.statistics.sunnyDays / reportData.forecast.length) * 100)}%</div>
                <div class="stat-label">Probabilidad de Sol</div>
            </div>
        </div>
    `;
}

function getHumidityDescription(humidity) {
    if (humidity < 30) return 'muy secas';
    if (humidity < 50) return 'secas';
    if (humidity < 70) return 'cómodas';
    if (humidity < 85) return 'húmedas';
    return 'muy húmedas';
}

function getPressureDescription(pressure) {
    if (pressure < 1000) return 'Baja (Inestable)';
    if (pressure < 1013) return 'Normal-Baja';
    if (pressure < 1020) return 'Normal';
    return 'Alta (Estable)';
}

function getDayName(date) {
    const days = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
    return days[date.getDay()];
}

// Add pulse animation for radar dots and location indicator
const pulseStyle = document.createElement('style');
pulseStyle.textContent = `
    @keyframes pulse {
        0%, 100% { opacity: 0.8; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(1.2); }
    }
    
    @keyframes locationIndicatorSlide {
        0% { 
            transform: translateX(-50%) translateY(-20px); 
            opacity: 0; 
        }
        100% { 
            transform: translateX(-50%) translateY(0); 
            opacity: 1; 
        }
    }
    
    @keyframes locationIndicatorFadeOut {
        0% { 
            transform: translateX(-50%) translateY(0); 
            opacity: 1; 
        }
        100% { 
            transform: translateX(-50%) translateY(-20px); 
            opacity: 0; 
        }
    }
`;
document.head.appendChild(pulseStyle);