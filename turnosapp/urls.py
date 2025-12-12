from django.urls import path
from . import views

urlpatterns = [
    # vista pública (cliente)
    path("", views.solicitar_turno, name="solicitar_turno"),

    # autenticación
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),

    # panel privado y CRUD
    path("panel/", views.panel_turnos, name="panel"),
    path("turnos/crear/", views.crear_turno, name="crear_turno"),
    path("turnos/<int:pk>/editar/", views.editar_turno, name="editar_turno"),
    path("turnos/<int:pk>/eliminar/", views.eliminar_turno, name="eliminar_turno"),
    path("turnos/<int:pk>/llamar/", views.llamar_turno, name="llamar_turno"),
    path("turnos/<int:pk>/atender/", views.marcar_atendido, name="marcar_atendido"),
]
