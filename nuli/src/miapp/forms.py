from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Editar_Perfil, Mes

class UsuModelForm(forms.ModelForm):
    class Meta():
        model = Editar_Perfil
        fields  = ['sexo','edad','peso','altura','objetivo','actividad']

class MesModelForm(forms.ModelForm):
    class Meta():
        model = Mes
        fields = ["mes"]

class UserCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None