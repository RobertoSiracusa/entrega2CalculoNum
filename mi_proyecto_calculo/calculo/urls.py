# mi_proyecto_calculo/calculo/urls.py

from django.urls import path
from . import views # Importa las vistas de esta misma app

app_name = 'calculo' # Opcional, pero buena práctica para nombrar URLs

urlpatterns = [
    path('', views.grafica_3d_view, name='grafica_3d'),
    path('ejecutar/', views.ejecutar_main_view, name='ejecutar_main'),
    path('reset/', views.reset_execution_count_view, name='reset_counter'),
    path('download/<str:filename>/', views.download_file_view, name='download_file'),
]