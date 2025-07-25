# mi_proyecto_calculo/mi_proyecto_calculo/urls.py
# mi_proyecto_calculo/mi_proyecto_calculo/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView # <-- Nueva importación

urlpatterns = [
    path('admin/', admin.site.urls),
    path('calculo/', include('calculo.urls')),
    path('', RedirectView.as_view(url='calculo/', permanent=False)), # <-- Opcional: usar RedirectView
]