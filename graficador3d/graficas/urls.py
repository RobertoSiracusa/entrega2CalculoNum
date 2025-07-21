from django.urls import path
from . import views

urlpatterns = [
    path('', views.grafica_3d, name='grafica_3d'),
]
