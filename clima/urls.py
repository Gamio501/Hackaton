from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_osm, name='index'),  # Redirigir a OpenStreetMap por defecto
    path('osm/', views.index_osm, name='index_osm'),
    path('pronostico/<int:registro_id>/', views.pronostico, name='pronostico'),
    path('historial/', views.historial, name='historial'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/pronostico/<int:registro_id>/', views.api_pronostico, name='api_pronostico'),
    path('visual/', views.visual, name='visual'),
    # URLs de autenticación
    path('login/', views.login_simple, name='login_page'),
    path('login/auth/', views.login_auth, name='login_auth'),
    path('register/', views.register_user, name='register_user'),
    path('logout/', views.logout, name='logout'),
    path('check-auth/', views.check_auth, name='check_auth'),
    path('test-api/', views.test_api, name='test_api'),
]
