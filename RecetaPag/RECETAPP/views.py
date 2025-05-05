from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .forms import RecetaForm
from .models import Receta, comentario, Favorito
from .forms import ComentarioForm
from django.db.models import Avg, Q
from django.http import JsonResponse

# Create your views here.

def principal(request):
    return render(request, "index.html")

def recetas(request):
    consulta = request.GET.get('busqueda', '')
    recetas = Receta.objects.all()

    if consulta:
        recetas = recetas.filter(titulo__icontains=consulta)

    for receta in recetas:
        # Calcular el promedio de calificaciones para cada receta
        promedio = receta.comentarios.aggregate(Avg('calificacion'))['calificacion__avg']
        # Si no hay calificaciones, asignar un mensaje
        if promedio is None:
            receta.promedio = "Sin calificaciones aún"
        else:
            receta.promedio = round(promedio, 1)

    return render(request, 'recetas_list.html', {'recetas': recetas})


def favoritas(request):
    favoritos = Favorito.objects.filter(usuario=request.user)
    return render(request, 'recetas_fav.html', {'favoritos': favoritos})

@login_required
def login_page(request):
   return render(request, 'registration/login.html')

@login_required
def pagprincipal(request):
    return render(request, "pagPrincipal.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirigir_usuario(request)  # Redirige según el tipo de usuario
        else:
            return render(request, "registration/login.html", {"error": "Usuario o contraseña incorrectos"})  

    return render(request, "registration/login.html")

def registro(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/accounts/login/")
    else:
        form = CustomUserCreationForm()

    return render(request, "registro.html", {"form": form})

def redirigir_usuario(request):
    if request.user.is_superuser:
        return redirect('pagprincipal')  # Redirige al panel de administración
    elif request.user.is_staff:
        return redirect('psicologo')  # Redirige a la página de psicólogos
    else:
        return redirect('pagPrincipal.html') 

@login_required
def mis_recetas(request):
    recetas = Receta.objects.filter(usuario=request.user)
    return render(request, 'mis_recetas.html', {'recetas': recetas})

@login_required
def crear_receta(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.usuario = request.user
            receta.save()
            return redirect('mis_recetas')
    else:
        form = RecetaForm()
    return render(request, 'crear_receta.html', {'form': form})

@login_required
def editar_receta(request, id):
    receta = get_object_or_404(Receta, id=id, usuario=request.user)
    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        if form.is_valid():
            form.save()
            return redirect('mis_recetas')
    else:
        form = RecetaForm(instance=receta)
    return render(request, 'crear_receta.html', {'form': form})

@login_required
def eliminar_receta(request, id):
    receta = get_object_or_404(Receta, id=id, usuario=request.user)
    receta.delete()
    return redirect('mis_recetas')

def detalle_receta(request, receta_id):
    receta = get_object_or_404(Receta, id=receta_id)
    comentarios = receta.comentarios.all()
    promedio = comentarios.aggregate(Avg('calificacion'))['calificacion__avg']

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.receta = receta
            comentario.save()
            return redirect('detalle_receta', receta_id=receta.id)
    else:
        form = ComentarioForm()

    return render(request, 'detalle_receta.html', {
        'receta': receta,
        'comentarios': comentarios,
        'promedio': promedio,
        'form': form
    })

def agregar_a_favoritos(request, id):
    receta = get_object_or_404(Receta, id=id)
    Favorito.objects.get_or_create(usuario=request.user, receta=receta)
    return redirect('recetas')  # O redirige a donde prefieras