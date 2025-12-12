from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegistroForm, SolicitarTurnoForm, TurnoForm
from .models import Turno


# ---------- AUTENTICACIÓN ----------


def register_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistroForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("panel")
        else:
            error = "Usuario o contraseña incorrectos."

    return render(request, "login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("login")


# ---------- VISTAS PRIVADAS (CRUD TURNOS) ----------


@login_required
def panel_turnos(request):
    turnos = Turno.objects.all().order_by("numero")
    atendidos = turnos.filter(estado="ATENDIDO").count()
    contexto = {
        "turnos": turnos,
        "atendidos": atendidos,
    }
    return render(request, "panel.html", contexto)


@login_required
def crear_turno(request):
    if request.method == "POST":
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("panel")
    else:
        max_numero = Turno.objects.aggregate(Max("numero"))["numero__max"] or 0
        form = TurnoForm(initial={"estado": "EN_ESPERA", "numero": max_numero + 1})

    return render(
        request,
        "turno_form.html",
        {"form": form, "titulo": "Crear Turno"},
    )


@login_required
def editar_turno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)
    if request.method == "POST":
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect("panel")
    else:
        form = TurnoForm(instance=turno)

    return render(
        request,
        "turno_form.html",
        {"form": form, "titulo": "Editar Turno"},
    )


@login_required
def eliminar_turno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)
    if request.method == "POST":
        turno.delete()
        return redirect("panel")
    return render(request, "turno_confirm_delete.html", {"turno": turno})


@login_required
def llamar_turno(request, pk):
    turno = get_object_or_404(Turno, pk=pk)
    turno.estado = "LLAMADO"
    turno.save()
    return redirect("panel")


@login_required
def marcar_atendido(request, pk):
    turno = get_object_or_404(Turno, pk=pk)
    turno.estado = "ATENDIDO"
    turno.save()
    return redirect("panel")


# ---------- VISTA PÚBLICA: SOLICITAR TURNO ----------


def solicitar_turno(request):
    turno_creado = None
    personas_delante = None
    tiempo_estimado = None  # en minutos (ejemplo: 10 por persona)

    if request.method == "POST":
        form = SolicitarTurnoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            telefono = form.cleaned_data["telefono"]

            max_numero = Turno.objects.aggregate(Max("numero"))["numero__max"] or 0
            numero_nuevo = max_numero + 1

            turno_creado = Turno.objects.create(
                numero=numero_nuevo,
                nombre=nombre,
                telefono=telefono,
                estado="EN_ESPERA",
            )

            personas_delante = Turno.objects.filter(
                estado__in=["EN_ESPERA", "LLAMADO"],
                numero__lt=numero_nuevo,
            ).count()

            tiempo_estimado = personas_delante * 10
    else:
        form = SolicitarTurnoForm()

    contexto = {
        "form": form,
        "turno_creado": turno_creado,
        "personas_delante": personas_delante,
        "tiempo_estimado": tiempo_estimado,
    }
    return render(request, "solicitar_turno.html", contexto)
