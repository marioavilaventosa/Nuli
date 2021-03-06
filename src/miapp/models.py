from django import forms
from django.db import models
from django.contrib.auth.models import User
import datetime
import locale
from django.urls import reverse
from django.core.files.storage import FileSystemStorage

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to = "static/img", blank=True, null=True)
    video_url = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('detalle_ejercicio', args=[self.nombre])

    def get_video_url(self):
        url = self.video_url.split("=")[-1]
        return url

class EjercicioDia(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    ejercicios = models.ManyToManyField(Ejercicio)
    musculo = models.CharField(max_length=100, blank=True, null=True)
    foto = models.ImageField(upload_to = "static/img", blank=True, null=True)
    num_ejercicios = models.CharField(max_length=100, blank=True, null=True)
    tiempo = models.CharField(max_length=100, blank=True, null=True)
    informativo = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('detalle_dia', args=[self.nombre])

    def get_nombre(self):
        return self.nombre.split(" ")[0]


class Entrenamiento(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    dias = models.ManyToManyField(EjercicioDia)
    DEFINICION = 'Definicion'
    MANTENIMIENTO = 'Mantenimiento'
    MUSCULACION = 'Musculacion'
    elecciones_objetivo = [ (DEFINICION, 'Definicion'), (MANTENIMIENTO, 'Mantenimiento'), (MUSCULACION, 'Musculacion') ]
    objetivo = models.CharField(max_length=13,choices=elecciones_objetivo, default=MANTENIMIENTO,)
    num_dias = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('detalle_entrenamiento', args=[self.nombre])


class Frase(models.Model):
    lema = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.lema

class Editar_Perfil(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    HOMBRE = 'Hombre'
    MUJER = 'Mujer'
    elecciones_sexo = [ (HOMBRE, 'Hombre'), (MUJER, 'Mujer'),]
    sexo = models.CharField(max_length=6,choices=elecciones_sexo, default=HOMBRE,)
    edad = models.IntegerField(default=18)
    peso = models.DecimalField(default=60,max_digits=3, decimal_places=1)
    altura = models.IntegerField(default=180)
    DEFINICION = 'Definicion'
    MANTENIMIENTO = 'Mantenimiento'
    MUSCULACION = 'Musculacion'
    elecciones_objetivo = [ (DEFINICION, 'Definicion'), (MANTENIMIENTO, 'Mantenimiento'), (MUSCULACION, 'Musculacion') ]
    objetivo = models.CharField(max_length=13,choices=elecciones_objetivo, default=MANTENIMIENTO,)
    NADA = 'Nada de ejercicio'
    LIGERO = 'Ejercicio Ligero'
    MODERADO = 'Ejercicio Moderado'
    REGULAR = 'Ejercicio Regular'
    INTENSO = 'Ejercicio Intenso'
    elecciones_actividad = [ (NADA, 'Nada de ejercicio'), (LIGERO, 'Ejercicio Ligero'), (MODERADO, 'Ejercicio Moderado'), (REGULAR, 'Ejercicio Regular'), (INTENSO, 'Ejercicio Intenso') ]
    actividad = models.CharField(max_length=50,choices=elecciones_actividad, default=MODERADO,)
    ejercicios = models.ForeignKey(Entrenamiento,on_delete=models.CASCADE,null=True)
    frase = models.ForeignKey(Frase,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.usuario)

class Año(models.Model):
    numero_año = models.CharField(max_length=100, blank=True, null=True)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    enero = models.CharField(max_length=124, default="0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    febrero = models.CharField(max_length=112, default="0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    marzo = models.CharField(max_length=124, default="0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    abril = models.CharField(max_length=124, default="000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    mayo = models.CharField(max_length=124, default="0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    junio = models.CharField(max_length=124, default="000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    julio = models.CharField(max_length=124, default="0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    agosto = models.CharField(max_length=124, default="0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    septiembre = models.CharField(max_length=124, default="000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    octubre = models.CharField(max_length=124, default="0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    noviembre = models.CharField(max_length=124, default="000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    diciembre = models.CharField(max_length=124, default="0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000")
    ultimo_dia = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.numero_año

class Mes(models.Model):
    ENERO = 'Enero'
    FEBRERO = 'Febrero'
    MARZO = 'Marzo'
    ABRIL = 'Abril'
    MAYO = 'Mayo'
    JUNIO = 'Junio'
    JULIO = 'Julio'
    AGOSTO = 'Agosto'
    SEPTIEMBRE = 'Septiembre'
    OCTUBRE = 'Octubre'
    NOVIEMBRE = 'Noviembre'
    DICIEMBRE = 'Diciembre'
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    mes = datetime.datetime.now()
    mes = mes.strftime('%B').capitalize()
    elecciones_mes = [ (ENERO, 'Enero'), (FEBRERO, 'Febrero'), (MARZO, 'Marzo'), (ABRIL, 'Abril'), (MAYO, 'Mayo'), (JUNIO, 'Junio'), (JULIO, 'Julio'), (AGOSTO, 'Agosto'), (SEPTIEMBRE, 'Septiembre'), (OCTUBRE, 'Octubre'), (NOVIEMBRE, 'Noviembre'), (DICIEMBRE, 'Diciembre') ]
    mes = models.CharField(max_length=50,choices=elecciones_mes, default=mes,)
