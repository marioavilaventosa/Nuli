from django.contrib import admin

# Register your models here.
from .forms import UsuModelForm
from .models import Editar_Perfil, Entrenamiento, EjercicioDia, Ejercicio, Frase, Año

#Aquí están las clases que queremos administrar desde el panel de admin

class AdminEditar_Perfil(admin.ModelAdmin):
    list_display = ["usuario","sexo","edad","peso",'altura','objetivo','actividad','ejercicios']
    form = UsuModelForm
    list_filter = ['sexo',"edad","peso",'objetivo']

class AdminEntrenamiento(admin.ModelAdmin):
    list_display = ["nombre",'objetivo','num_dias']
    list_editable = ['objetivo','num_dias']

class AdminEjercicioDia(admin.ModelAdmin):
    list_display = ["nombre","musculo","foto",'num_ejercicios','tiempo','informativo']
    list_editable = ["musculo","foto",'informativo']

class AdminEjercicio(admin.ModelAdmin):
    list_display = ["nombre","foto"]
    list_editable = ["foto"]
    list_display_links = ["nombre"]

class AdminFrase(admin.ModelAdmin):
    list_display = ["lema"]
    list_editable = list_display
    list_display_links = None

class AdminAño(admin.ModelAdmin):
    list_display = ["numero_año","usuario","ultimo_dia"]
    list_editable = []


admin.site.register(Editar_Perfil, AdminEditar_Perfil)
admin.site.register(Entrenamiento, AdminEntrenamiento)
admin.site.register(EjercicioDia, AdminEjercicioDia)
admin.site.register(Ejercicio, AdminEjercicio)
admin.site.register(Frase, AdminFrase)
admin.site.register(Año, AdminAño)