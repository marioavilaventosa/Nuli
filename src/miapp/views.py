from django.shortcuts import render
from django import forms
import random
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
import datetime
import locale
from django.shortcuts import redirect

# Create your views here.

from .forms import UsuModelForm, UserCreateForm, MesModelForm
from .models import Editar_Perfil, Entrenamiento, Frase, Año, Ejercicio, EjercicioDia

class SignUp(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def inicio(request): 
    usuario = request.user
    if request.user.is_authenticated:
        #Si el usuario no ha editado su perfil le manda a editarlo
        entrenamiento = Editar_Perfil.objects.filter(usuario=usuario)
        if not entrenamiento:
            return redirect("editar_perfil")
        #-------------------
        # TO DO -------------------------------
        dia_actual = False
        #Si el campo "ultimo_dia" es el mismo dia que hoy convertir "dia_actual" a True
        hoy = datetime.datetime.today()
        hoy = hoy.strftime("%m/%d/%y")
        if Año.objects.filter(usuario=usuario).get().ultimo_dia == hoy:
            dia_actual = True
        frases = Frase.objects.all()
        frase = random.choice(frases)
        #Actualiza el valor de un campo
        Editar_Perfil.objects.filter(usuario=usuario).update(frase=frase)
        frase = Editar_Perfil.objects.filter(usuario=usuario).get().frase
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        ahora = datetime.datetime.now()
        ahora = ahora.strftime('%A').capitalize()
        entrenamiento = Editar_Perfil.objects.filter(usuario=usuario).get().ejercicios
        ejercicios = []
        descanso = True
        for dia in entrenamiento.dias.all():
            if ahora == dia.nombre.split(" ")[0]:
                descanso = False
                for ejercicio in dia.ejercicios.all():
                    ejercicios.append(ejercicio)
        context = {
            "frase": frase,
            "ejercicios": ejercicios,
            "descanso": descanso,
            "dia_actual": dia_actual,
            "ahora": ahora,
        }
    else:
        context = {
        }
    return render(request,"inicio.html", context)


def detalle_ejercicio(request, ejercicio):
    usuario = request.user
    if not usuario.is_anonymous:
        ejercicio = Ejercicio.objects.get(nombre=ejercicio)
        entrenamiento = Editar_Perfil.objects.filter(usuario=usuario)
        nombre = ejercicio.nombre
        nombre = nombre.split("|")
        nombre = nombre[0]
        if not entrenamiento:
            return redirect("editar_perfil")
        context = {
            "nombre": nombre,
            "ejercicio": ejercicio,
        }
    else:
        context = {

        }
    return render(request,"detalle_ejercicio.html", context)


def entrenamientos(request):
    usuario = request.user
    if not usuario.is_anonymous:
        entrenamiento = Editar_Perfil.objects.filter(usuario=usuario)
        if not entrenamiento:
            return redirect("editar_perfil")
        entrenamientos = Entrenamiento.objects.all()
        todos_entrenamientos = []
        todos = []
        for entrenamiento in entrenamientos:
            todos_entrenamientos.append(entrenamiento.nombre)
            for dia in entrenamiento.dias.all():
                todos.append(dia)
        
        context = {
            "entrenamientos": entrenamientos,
            "todos_entrenamientos": todos_entrenamientos,
            "todos": todos,
        }
    else:
        context = {

        }
    return render(request,"entrenamientos.html", context)

def detalle_entrenamiento(request, entrenamiento):
    usuario = request.user
    if not usuario.is_anonymous:
        entrenamiento = Entrenamiento.objects.get(nombre=entrenamiento)
        if not entrenamiento:
            return redirect("editar_perfil")
        context = {
            "entrenamiento": entrenamiento,
        }
    else:
        context = {

        }
    return render(request,"detalle_entrenamiento.html", context)


def detalle_dia(request, dia):
    usuario = request.user
    if not usuario.is_anonymous:
        dia = EjercicioDia.objects.get(nombre=dia)
        entrenamiento = Editar_Perfil.objects.filter(usuario=usuario)
        if not entrenamiento:
            return redirect("editar_perfil")
        context = {
            "dia": dia,
        }
    else:
        context = {

        }
    return render(request,"detalle_dia.html", context)


def tu_entrenamiento(request):
    if request.user.is_authenticated:
        usuario = request.user
        entrenamiento = Editar_Perfil.objects.filter(usuario=usuario)
        if not entrenamiento:
            return redirect("editar_perfil")
        entrenamiento = Editar_Perfil.objects.filter(usuario=usuario).get().ejercicios
        context =  {
            "entrenamiento": entrenamiento,
        }
    else:
        context = {

        }
    return render(request, "tu_entrenamiento.html", context)

def calculadora_calorias(request):
    if request.user.is_authenticated:
        usuario = request.user
        entrenamiento = Editar_Perfil.objects.filter(usuario=usuario)
        if not entrenamiento:
            return redirect("editar_perfil")
        tmb = 10 * float(Editar_Perfil.objects.filter(usuario=usuario).get().peso)
        tmb += 6.25 * float(Editar_Perfil.objects.filter(usuario=usuario).get().altura)
        tmb -= 5 * float(Editar_Perfil.objects.filter(usuario=usuario).get().edad)
        if Editar_Perfil.objects.filter(usuario=usuario).get().sexo == 'Hombre':
            tmb += 5
        else:
            tmb -= 161
        actividad = Editar_Perfil.objects.filter(usuario=usuario).get().actividad
        if actividad == 'Nada de ejercicio':
            tmb = tmb * 1.22
        elif actividad == 'Ejercicio Ligero':
            tmb = tmb * 1.375
        elif actividad == 'Ejercicio Moderado':
            tmb = tmb * 1.55
        elif actividad == 'Ejercicio Regular':
            tmb = tmb * 1.725
        elif actividad == 'Ejercicio Intenso':
            tmb = tmb * 1.9
        if Editar_Perfil.objects.filter(usuario=usuario).get().objetivo == 'Definicion':
            tmb -= 200
        elif Editar_Perfil.objects.filter(usuario=usuario).get().objetivo == 'Musculacion':
            tmb += 200
        tmb = int(tmb)
        context = {
            'tmb': tmb,
        }
    else:
        context = {

        }
    return render(request, "calculadora_calorias.html", context)

def editar_perfil(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    usuario = request.user
    #Comprueba si hay calendario para el
    calendario = Año.objects.filter(usuario=usuario)
    if not calendario:
        p = Año(numero_año=2019, usuario=usuario)
        p.save()
    #Comprueba si hay entrenamiento creado ya para el
    entrenamiento = Editar_Perfil.objects.filter(usuario=usuario)
    if entrenamiento:
        sexo = Editar_Perfil.objects.filter(usuario=usuario).get().sexo
        edad = Editar_Perfil.objects.filter(usuario=usuario).get().edad
        peso = Editar_Perfil.objects.filter(usuario=usuario).get().peso
        altura = Editar_Perfil.objects.filter(usuario=usuario).get().altura
        objetivo = Editar_Perfil.objects.filter(usuario=usuario).get().objetivo
        actividad = Editar_Perfil.objects.filter(usuario=usuario).get().actividad
        form = UsuModelForm(request.POST or None, initial={'sexo': sexo, 'edad': edad, 'peso': peso, 'altura': altura, 'objetivo': objetivo, 'actividad': actividad})
    else:
        form = UsuModelForm(request.POST or None)
    if form.is_valid():
        if Editar_Perfil.objects.filter(usuario=usuario).exists():
            instance = form.save(commit=False)
            objetivo = instance.objetivo
            #Si cambia de objetivo le pongo otro entrenamiento
            if Editar_Perfil.objects.filter(usuario=usuario).get().objetivo != objetivo:
                valores = Entrenamiento.objects.filter(objetivo=objetivo)
                valor_aleatorio = random.choice(valores)
                #Cambiar el valor de una casilla
                instance.ejercicios = valor_aleatorio
            else:
                #Como no ha cambiado de objetivo se queda el mismo
                instance.ejercicios = Editar_Perfil.objects.filter(usuario=usuario).get().ejercicios
            #Consigo el usuario 
            instance.usuario = request.user
            #Elimino el registro del usuario
            Editar_Perfil.objects.filter(usuario=usuario).delete()
            instance.save()
        else:
            instance = form.save(commit=False)
            objetivo = instance.objetivo
            valores = Entrenamiento.objects.filter(objetivo=objetivo)
            valor_aleatorio = random.choice(valores)
            #Cambiar el valor de una casilla
            instance.ejercicios = valor_aleatorio
            instance.usuario = request.user
            instance.save()
        return HttpResponseRedirect('/')
    context = {
        "form": form,
    }
    return render(request,"editar_perfil.html", context)

def progreso(request):
    if request.user.is_authenticated:
        usuario = request.user
        form = MesModelForm(request.POST or None)
        instance = form.save(commit=False)
        mes = instance.mes
        if mes == "Enero":
            cambio = Año.objects.filter(usuario=usuario).get().enero
            dias = 31*4
        elif mes == "Febrero":
            cambio = Año.objects.filter(usuario=usuario).get().febrero
            dias = 28*4
        elif mes == "Marzo":
            cambio = Año.objects.filter(usuario=usuario).get().marzo
            dias = 31*4
        elif mes == "Abril":
            cambio = Año.objects.filter(usuario=usuario).get().abril
            dias = 30*4
        elif mes == "Mayo":
            cambio = Año.objects.filter(usuario=usuario).get().mayo
            dias = 31*4
        elif mes == "Junio":
            cambio = Año.objects.filter(usuario=usuario).get().junio
            dias = 30*4
        elif mes == "Julio":
            cambio = Año.objects.filter(usuario=usuario).get().julio
            dias = 31*4
        elif mes == "Agosto":
            cambio = Año.objects.filter(usuario=usuario).get().agosto
            dias = 31*4
        elif mes == "Septiembre":
            cambio = Año.objects.filter(usuario=usuario).get().septiembre
            dias = 30*4
        elif mes == "Octubre":
            cambio = Año.objects.filter(usuario=usuario).get().octubre
            dias = 31*4
        elif mes == "Noviembre":
            cambio = Año.objects.filter(usuario=usuario).get().noviembre
            dias = 30*4
        elif mes == "Diciembre":
            cambio = Año.objects.filter(usuario=usuario).get().diciembre
            dias = 31*4
        separado = []
        intervalo = 0
        for i in range(1,dias+1):
            if i%4 == 0:
                cal_dia = cambio[intervalo:i]
                if cal_dia == "0000":
                    cal_dia = "0"
                else:
                    cuenta = 0
                    while cal_dia[0] == "0":
                        cuenta += 1
                        cal_dia = cal_dia[cuenta:]
                lista = []
                lista.append(str(int(cal_dia)//3))
                lista.append(cal_dia)
                separado.append(lista)
                intervalo += 4
        context = {
            "form": form,
            "cambio": cambio,
            'separado': separado,
            "dias": range(1,int(dias+4)//4),
            "mes": mes.capitalize(),
        }
    else:
        context = {
            
        }
    return render(request,"progreso.html", context, )

def terminar_entrenamiento(request):
    usuario = request.user
    #Tengo que coger las calorías de su sesion de entrenamiento del día de hoy multiplicando los minutos por 5.25 (caloria el minuto)
    ahora = datetime.datetime.now()
    ahora = ahora.strftime('%A').capitalize()
    entrenamiento = Editar_Perfil.objects.filter(usuario=usuario).get().ejercicios
    calorias = ""
    for dia in entrenamiento.dias.all():
        if ahora == dia.get_nombre():
            calorias = dia.tiempo
            calorias = calorias.split(" ")[0]
            calorias = int(50 * 5.25)
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    #Coger el numero del dia de hoy
    dia = datetime.datetime.today()
    dia = dia.day
    #Coger el numero del mes de hoy
    mes = datetime.datetime.now()
    mes = mes.strftime('%B')
    #Cambiar al mes correspondiente las calorias del entrenamiento
    if mes == "enero":
        cambio = Año.objects.filter(usuario=usuario).get().enero
    elif mes == "febrero":
        cambio = Año.objects.filter(usuario=usuario).get().febrero
    elif mes == "marzo":
        cambio = Año.objects.filter(usuario=usuario).get().marzo
    elif mes == "abril":
        cambio = Año.objects.filter(usuario=usuario).get().abril
    elif mes == "mayo":
        cambio = Año.objects.filter(usuario=usuario).get().mayo
    elif mes == "junio":
        cambio = Año.objects.filter(usuario=usuario).get().junio
    elif mes == "julio":
        cambio = Año.objects.filter(usuario=usuario).get().julio
    elif mes == "agosto":
        cambio = Año.objects.filter(usuario=usuario).get().agosto
    elif mes == "septiembre":
        cambio = Año.objects.filter(usuario=usuario).get().septiembre
    elif mes == "octubre":
        cambio = Año.objects.filter(usuario=usuario).get().octubre
    elif mes == "noviembre":
        print("yes")
        cambio = Año.objects.filter(usuario=usuario).get().noviembre
    elif mes == "diciembre":
        cambio = Año.objects.filter(usuario=usuario).get().diciembre
    #Se convierte el texto a lista para poder cambiar las calorias
    lista = list(cambio)
    #Se cambian las calorias
    intervalo = (dia-1)*4
    calorias = str(calorias)
    ceros = 4 - len(calorias)
    ceros = ceros * "0"
    calorias = ceros + calorias     
    lista[intervalo:intervalo+1] = calorias[0]
    lista[intervalo+1:intervalo+2] = calorias[1]
    lista[intervalo+2:intervalo+3] = calorias[2]
    lista[intervalo+3:intervalo+4] = calorias[3]
    #Se convierte de nuevo a texto
    cambio = "".join(lista)
    print(mes)
    #Cambiar el mes
    if mes == "enero":
        Año.objects.filter(usuario=usuario).update(enero=cambio)
    elif mes == "febrero":
        Año.objects.filter(usuario=usuario).update(febrero=cambio)
    elif mes == "marzo":
        Año.objects.filter(usuario=usuario).update(marzo=cambio)
    elif mes == "abril":
        Año.objects.filter(usuario=usuario).update(abril=cambio)
    elif mes == "mayo":
        Año.objects.filter(usuario=usuario).update(mayo=cambio)
    elif mes == "junio":
        Año.objects.filter(usuario=usuario).update(junio=cambio)
    elif mes == "julio":
        Año.objects.filter(usuario=usuario).update(julio=cambio)
    elif mes == "agosto":
        Año.objects.filter(usuario=usuario).update(agosto=cambio)
    elif mes == "septiembre":
        Año.objects.filter(usuario=usuario).update(septiembre=cambio)
    elif mes == "octubre":
        Año.objects.filter(usuario=usuario).update(octubre=cambio)
    elif mes == "noviembre":
        print("yes2")
        Año.objects.filter(usuario=usuario).update(noviembre=cambio)
    elif mes == "diciembre":
        Año.objects.filter(usuario=usuario).update(diciembre=cambio)
    #Cambiar el "ultimo_dia" al dia de hoy
    hoy = datetime.datetime.today()
    hoy = hoy.strftime("%m/%d/%y")
    Año.objects.filter(usuario=usuario).update(ultimo_dia=hoy)
    #Redirigir al inicio
    return redirect('/')

def error_500(request):
    return redirect('/')
