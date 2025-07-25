# mi_proyecto_calculo/calculo/urls.py

from django.urls import path
from . import views # Importa las vistas de esta misma app

app_name = 'calculo' # Opcional, pero buena práctica para nombrar URLs

urlpatterns = [
    path('', views.grafica_3d_view, name='grafica_3d'), # <-- Nuestra primera URL
]