from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from .models import Carona, Usuario, Avaliacao
from .forms import CadastroForm, LoginForm, UsuarioForm, CaronaForm, AvaliacaoForm

# ------------------------------
# Página inicial
# ------------------------------
def index(request):
    return render(request, "index.html")


# ------------------------------
# Cadastro de usuário
# ------------------------------
def cadastro_usuario(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect("login")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = CadastroForm()
    return render(request, "cadastro.html", {"form": form})


# ------------------------------
# Login de usuário
# ------------------------------
def login_usuario(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            senha = form.cleaned_data['password']

            # Autenticação via email ou username
            try:
                user_obj = Usuario.objects.get(email=username_or_email)
                usuario = authenticate(request, username=user_obj.username, password=senha)
            except Usuario.DoesNotExist:
                usuario = authenticate(request, username=username_or_email, password=senha)

            if usuario:
                login(request, usuario)
                messages.success(request, "Login realizado com sucesso!")
                return redirect("index")
            else:
                messages.error(request, "Usuário ou senha incorretos!")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


# ------------------------------
# Logout
# ------------------------------
def logout_usuario(request):
    logout(request)
    return redirect("index")


# ------------------------------
# Listagem de caronas
# ------------------------------
def lista_caronas(request):
    caronas = Carona.objects.all().order_by("data")
    
    # Filtros simples
    cidade_partida = request.GET.get('cidade_partida')
    cidade_destino = request.GET.get('cidade_destino')
    data = request.GET.get('data')

    if cidade_partida:
        caronas = caronas.filter(cidade_partida__icontains=cidade_partida)
    if cidade_destino:
        caronas = caronas.filter(cidade_destino__icontains=cidade_destino)
    if data:
        caronas = caronas.filter(data=data)

    return render(request, "lista_caronas.html", {"caronas": caronas})


# ------------------------------
# Publicar nova carona
# ------------------------------
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
    return render(request, "publicar_carona.html", {"form": form})


# ------------------------------
# Detalhes da carona
# ------------------------------
def detalhes_carona(request, id_carona):
    carona = get_object_or_404(Carona, id=id_carona)
    return render(request, "detalhes_carona.html", {"carona": carona})


# ------------------------------
# Redirecionar para WhatsApp
# ------------------------------
def redirecionar_whatsapp(request, id_carona):
    carona = get_object_or_404(Carona, id=id_carona)
    numero = carona.usuario.telefone if hasattr(carona.usuario, 'telefone') else "000000000"
    return redirect(f"https://wa.me/{numero}?text=Olá, vi sua carona para {carona.cidade_destino} no Vai e Vem!")


# ------------------------------
# Perfil do usuário
# ------------------------------
def perfil_usuario(request):
    return render(request, "perfil_usuario.html", {"usuario": request.user})


def editar_perfil(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect("perfil_usuario")
    else:
        form = UsuarioForm(instance=request.user)
    return render(request, "editar_perfil.html", {"form": form})


def atualizar_foto(request):
    if request.method == "POST" and request.FILES.get('foto'):
        request.user.profile.image = request.FILES['foto']
        request.user.profile.save()
        messages.success(request, "Foto atualizada com sucesso!")
    return redirect("perfil_usuario")


# ------------------------------
# Minhas caronas
# ------------------------------
def minhas_caronas(request):
    caronas = Carona.objects.filter(usuario=request.user).order_by("data")
    return render(request, "minhas_caronas.html", {"caronas": caronas})


# ------------------------------
# Solicitar vaga em carona
# ------------------------------
def solicitar_vaga(request, id_carona):
    carona = get_object_or_404(Carona, id=id_carona)
    # Aqui você pode adicionar lógica para criar uma solicitação de vaga
    messages.success(request, "Solicitação de vaga enviada com sucesso!")
    return redirect("detalhes_carona", id_carona=id_carona)


# ------------------------------
# Avaliar usuário
# ------------------------------
def avaliar_usuario(request, id_usuario):
    usuario_avaliado = get_object_or_404(Usuario, id=id_usuario)
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
    return render(request, "avaliar_usuario.html", {"form": form, "usuario": usuario_avaliado})


def salvar_avaliacao(request, id_usuario):
    usuario_avaliado = get_object_or_404(Usuario, id=id_usuario)
    if request.method == "POST":
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.avaliador = request.user
            avaliacao.avaliado = usuario_avaliado
            avaliacao.save()
            messages.success(request, "Avaliação registrada com sucesso!")
    return redirect("lista_caronas")


# ------------------------------
# Home
# ------------------------------
def home(request):
    return render(request, "home.html")

