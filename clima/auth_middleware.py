from django.shortcuts import redirect
from django.urls import reverse

class AuthMiddleware:
    """Middleware para verificar autenticación en rutas protegidas"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        current_path = request.path
        
        # Rutas que requieren autenticación
        protected_paths = [
            '/',           # Página principal
            '/osm/',       # OpenStreetMap
            '/nasa/',      # NASA
            '/dashboard/', # Dashboard
            '/historial/', # Historial
        ]
        
        # Rutas que no requieren autenticación (exactas)
        public_paths = [
            '/visual/',
            '/login/',
            '/logout/',
            '/static/',
            '/admin/',
        ]
        
        # APIs que no requieren autenticación
        api_paths = [
            '/login/auth/',
            '/register/',
            '/check-auth/',
            '/api/',
        ]
        
        # Verificar si la ruta está protegida
        is_protected = any(current_path.startswith(path) for path in protected_paths)
        is_public = current_path in public_paths
        is_api = any(current_path.startswith(path) for path in api_paths)
        
        # Solo aplicar autenticación a rutas protegidas
        if is_protected and not request.session.get('usuario_autenticado'):
            # Evitar bucle de redirección
            if current_path != '/login/':
                return redirect('/login/')
        
        # Si está en login pero ya está autenticado, redirigir a home
        if current_path == '/login/' and request.session.get('usuario_autenticado'):
            return redirect('/')
        
        response = self.get_response(request)
        return response
