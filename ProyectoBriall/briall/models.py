from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Oficina(models.Model):
    equipamiento = models.CharField(max_length=300)
    capacidad = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=300)
    ubicacion = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=0)
    fecha = models.DateField()
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='media/oficinas', null=True, blank=True)


class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    oficina = models.ForeignKey(Oficina, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
