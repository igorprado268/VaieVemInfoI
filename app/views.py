from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from .models import Carona, Usuario, Avaliacao
from .forms import UsuarioForm, CaronaForm, AvaliacaoForm

# Página inicial
def index(request):
    return render(request, "index.html")


# Cadastro de usuário
def cadastro_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data["senha"])  # Criptografa senha
            usuario.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("login")
    else:
        form = UsuarioForm()
    return render(request, "usuarios/cadastro.html", {"form": form})


# Login de usuário
def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        usuario = authenticate(request, email=email, password=senha)
        if usuario:
            login(request, usuario)
            return redirect("index")
        else:
            messages.error(request, "Email ou senha incorretos!")
    return render(request, "usuarios/login.html")


# Logout
def logout_usuario(request):
    logout(request)
    return redirect("index")


# Listagem de caronas
def lista_caronas(request):
    caronas = Carona.objects.all().order_by("data")
    return render(request, "caronas/lista.html", {"caronas": caronas})


# Publicar nova carona
def publicar_carona(request):
    if request.method == "POST":
        form = CaronaForm(request.POST)
        if form.is_valid():
            carona = form.save(commit=False)
            carona.usuario = request.user
            carona.save()
            messages.success(request, "Carona publicada com sucesso!")
            return redirect("lista_caronas")
    else:
        form = CaronaForm()
    return render(request, "caronas/nova.html", {"form": form})


# Detalhes da carona
def detalhes_carona(request, id_carona):
    carona = get_object_or_404(Carona, id_carona=id_carona)
    return render(request, "caronas/detalhes.html", {"carona": carona})


# Redirecionar para WhatsApp
def redirecionar_whatsapp(request, id_carona):
    carona = get_object_or_404(Carona, id_carona=id_carona)
    numero = carona.usuario.username  # Aqui podemos usar o telefone se tiver no modelo
    return redirect(f"https://wa.me/{numero}?text=Olá, vi sua carona para {carona.destino} no Vai e Vem!")


# Avaliar usuário
def avaliar_usuario(request, id_usuario):
    usuario_avaliado = get_object_or_404(Usuario, id_usuario=id_usuario)
    if request.method == "POST":
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.avaliador = request.user
            avaliacao.avaliado = usuario_avaliado
            avaliacao.save()
            messages.success(request, "Avaliação registrada com sucesso!")
            return redirect("lista_caronas")
    else:
        form = AvaliacaoForm()
    return render(request, "avaliacoes/avaliar.html", {"form": form, "usuario": usuario_avaliado})
