from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Oficina, Reserva
from django.contrib.auth.decorators import login_required
#from .forms import ReservaForm, EliminarReservaForm
from django.shortcuts import render, redirect
from .forms import OficinaForm, ReservaForm
from .models import Oficina
from .forms import OficinaForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from .forms import ReservaForm
from django.db import IntegrityError
from .forms import RegistroForm


def reserva_reagendada_exitosa(request):
    return render(request, 'reserva_reagendada_exitosa.html')

def reserva_reagendada(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    if request.user == reserva.usuario:
        if request.method == 'POST':
            form = ReservaForm(request.POST, instance=reserva)
            if form.is_valid():
                form.save()
                return redirect('reserva_reagendada_exitosa')
        else:
            form = ReservaForm(instance=reserva)
            return render(request, 'reagendar_reserva.html', {'form': form})
    else:
        return redirect('reservas')

def reserva_cancelada(request):
    return render(request, 'reserva_cancelada.html')

def mis_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'mis_reservas.html', {'reservas': reservas})

def reagendar_reserva(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    if request.user == reserva.usuario:
        form = ReservaForm(instance=reserva)
        return render(request, 'reagendar_reserva.html', {'form': form, 'reserva': reserva})
    else:
        messages.error(request, "No tienes permiso para reagendar esta reserva.")
        return redirect('reservas')


def cancelar_reserva(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    if request.user == reserva.usuario:
        reserva.delete()
        return redirect('reserva_cancelada')
    else:
        messages.error(request, "No tienes permiso para cancelar esta reserva.")
        return redirect('mis_reservas')



def reserva_exitosa(request):
    return render(request, 'reserva_exitosa.html')

@login_required
def agendar_reserva(request, oficina_id):  # Cambiado id_oficina a oficina_id
    oficina = get_object_or_404(Oficina, id=oficina_id)  # Cambiado id_oficina a oficina_id
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            fecha_reserva = form.cleaned_data['fecha_reserva']
            reserva_existente = Reserva.objects.filter(
                oficina=oficina,
                fecha_reserva=fecha_reserva
            ).exclude(id=form.instance.id if form.instance else None).first()

            if reserva_existente:
                mensaje_error = 'Ya existe una reserva para esta oficina en la misma fecha. Por favor elige otro día.'
                return render(request, 'agendar_reserva.html', {'form': form, 'oficina': oficina, 'mensaje_error': mensaje_error})

            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.oficina = oficina
            reserva.save()
            return redirect('reserva_exitosa')
    else:
        form = ReservaForm()
    return render(request, 'agendar_reserva.html', {'form': form, 'oficina': oficina})  
  
@login_required
def reservar_oficina(request, oficina_id):
    oficina = get_object_or_404(Oficina, pk=oficina_id)
    return render(request, 'agendar_reserva.html', {'oficina': oficina})



@login_required
def actualizar_oficina(request, oficina_id):
    oficina = get_object_or_404(Oficina, id=oficina_id)
    if request.method == 'POST':
        form = OficinaForm(request.POST, request.FILES, instance=oficina)
        if form.is_valid():
            form.save()
            return redirect('ver_oficinas')
    else:
        form = OficinaForm(instance=oficina)
    return render(request, 'actualizar_oficina.html', {'form': form, 'oficina': oficina})

def ver_oficinas(request):
    oficinas = Oficina.objects.filter(disponible=True)
    return render(request, 'ver_oficinas.html', {'oficinas': oficinas})

def crear_oficina(request):
    if request.method == 'POST':
        form = OficinaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ver_oficinas')
    else:
        form = OficinaForm()
    return render(request, 'crear_oficina.html', {'form': form})

def login_usuario(request):
    if request.method == 'GET':
        return render(request, 'login_usuario.html', {
        'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'login_usuario.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('ver_oficinas')



def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('login_usuario')
            except IntegrityError:
                return render(request, 'registro_usuario.html', {
                    'form': form,
                    "error": 'El usuario ya existe'
                })
        else:
            return render(request, 'registro_usuario.html', {
                'form': form,
                "error": "Las contraseñas no coinciden"
            })
    else:
        return render(request, 'registro_usuario.html', {
            'form': RegistroForm()
        })

def cerrar_sesion(request):
    logout(request)
    return redirect('index')


def index(request):
    return render(request, 'index.html')







