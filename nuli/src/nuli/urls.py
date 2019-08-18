"""nuli URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from miapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('registro/', views.SignUp.as_view(), name='registro'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('entrenamientos/', views.entrenamientos, name='entrenamientos'),
    path('tu_entrenamiento/', views.tu_entrenamiento, name='tu_entrenamiento'),
    path('calculadora_calorias/', views.calculadora_calorias, name='calculadora_calorias'),
    path('progreso/', views.progreso, name='progreso'),
    path('terminar_entrenamiento/', views.terminar_entrenamiento, name='terminar_entrenamiento'),
    #Todos los entrenamientos
    path('Entrenamiento_Fat_Burn/', views.Entrenamiento_Fat_Burn, name='Entrenamiento_Fat_Burn'),
    path('Entrenamiento_Fuera_Camiseta/', views.Entrenamiento_Fuera_Camiseta, name='Entrenamiento_Fuera_Camiseta'),
    path('Entrenamiento_Full_Body/', views.Entrenamiento_Full_Body, name='Entrenamiento_Full_Body'),
]
