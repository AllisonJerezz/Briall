from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import reservar_oficina, agendar_reserva


urlpatterns = [
    path('', views.index),
    path('index/', views.index, name="index"),
    path('login_usuario/', views.login_usuario, name="login_usuario"),
    path('registro/', views.registro, name="registro"),
    path('cerrar_sesion/', views.cerrar_sesion, name="cerrar_sesion"),
    path('crear_oficina/', views.crear_oficina, name="crear_oficina"),
    path('ver_oficinas/', views.ver_oficinas, name="ver_oficinas"),
    path('actualizar_oficina/<int:oficina_id>/', views.actualizar_oficina, name='actualizar_oficina'),
    path('reservar_oficina/<int:oficina_id>/', reservar_oficina, name='reservar_oficina'),
    path('agendar_reserva/<int:oficina_id>/', agendar_reserva, name='agendar_reserva'),
    path('reserva_exitosa/', views.reserva_exitosa, name='reserva_exitosa'),
    path('cancelar_reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('reagendar_reserva/<int:reserva_id>/', views.reagendar_reserva, name='reagendar_reserva'),
    path('mis_reservas/', views.mis_reservas, name='mis_reservas'),
    path('reserva_cancelada/', views.reserva_cancelada, name='reserva_cancelada'),
    path('reserva_reagendada/<int:reserva_id>/', views.reserva_reagendada, name='reserva_reagendada'),
    path('reserva_reagendada_exitosa/', views.reserva_reagendada_exitosa, name='reserva_reagendada_exitosa'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


