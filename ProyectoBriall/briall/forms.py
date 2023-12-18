from xml.dom import ValidationErr
from django import forms
from .models import Oficina, Reserva
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from .models import Reserva

class RegistroForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class OficinaForm(forms.ModelForm):
    class Meta:
        model = Oficina
        fields = '__all__'
        labels = {
            'imagen': 'Imagen',
            'descripcion': 'Descripcion',
            'equipamiento': 'Equipamiento',
            'capacidad': 'Capacidad',
            'ubicacion': 'Ubicacion',
            'valor': 'Valor',
            'fecha': 'Fecha',
            'disponible': 'Disponible'
        }

from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from .models import Reserva

class ReservaForm(forms.ModelForm):
    fecha_reserva = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'required': True})
    )

    class Meta:
        model = Reserva
        fields = ['fecha_reserva']
        labels = {
            'fecha_reserva': 'Fecha',
        }

    def clean_fecha_reserva(self):
        fecha_reserva = self.cleaned_data.get('fecha_reserva')
        if not fecha_reserva:
            raise ValidationError('La fecha de reserva no puede estar vacía.')
        if fecha_reserva <= date.today():
            raise ValidationError('La fecha de reserva debe ser al menos un día después de la fecha actual.')

        return fecha_reserva