from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Carona, Usuario, Avaliacao, SolicitacaoVaga
from .forms import CadastroForm, LoginForm, UsuarioForm, CaronaForm, AvaliacaoForm

# ------------------------------
# Página inicial
# ------------------------------
def index(request):
    return render(request, "index.html")

def cadastro_usuario(request):
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Usuário cadastrado com sucesso! Faça login para continuar.")
            return redirect("login")
        else:
            # Mostra erros do formulário
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CadastroForm()
    
    return render(request, "cadastro.html", {"form": form})


def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("username")  # O campo do form se chama username
        senha = request.POST.get("password")

        # Autentica usando email (o backend customizado faz a conversão)
        user = authenticate(request, username=email, password=senha)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login realizado com sucesso!")
            return redirect("home")
        else:
            messages.error(request, "E-mail ou senha inválidos")
    
    return render(request, "login.html")


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
    
    cidade_partida = request.GET.get('cidade_partida')
    cidade_destino = request.GET.get('cidade_destino')
    data = request.GET.get('data')

    if cidade_partida:
        caronas = caronas.filter(origem__icontains=cidade_partida)
    if cidade_destino:
        caronas = caronas.filter(destino__icontains=cidade_destino)
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
    carona = get_object_or_404(Carona, id_carona=id_carona)
    solicitacoes = SolicitacaoVaga.objects.filter(carona=carona)
    return render(request, "detalhes_carona.html", {"carona": carona, "solicitacoes": solicitacoes})

# ------------------------------
# Redirecionar para WhatsApp
# ------------------------------
def redirecionar_whatsapp(request, id_carona):
    carona = get_object_or_404(Carona, id_carona=id_carona)
    numero = getattr(carona.usuario, 'telefone', '000000000')
    return redirect(f"https://wa.me/{numero}?text=Olá, vi sua carona para {carona.destino} no Vai e Vem!")

# ------------------------------
# Perfil do usuário
# ------------------------------
def perfil_usuario(request):
    caronas = Carona.objects.filter(usuario=request.user)
    avaliacoes = Avaliacao.objects.filter(avaliado=request.user)
    return render(request, "perfil_usuario.html", {
        "usuario": request.user,
        "caronas": caronas,
        "avaliacoes": avaliacoes
    })

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
        request.user.foto = request.FILES['foto']
        request.user.save()
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
    carona = get_object_or_404(Carona, id_carona=id_carona)
    SolicitacaoVaga.objects.create(carona=carona, usuario=request.user)
    messages.success(request, "Solicitação de vaga enviada com sucesso!")
    return redirect("detalhes_carona", id_carona=id_carona)

# ------------------------------
# Avaliar usuário
# ------------------------------
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
    return render(request, "avaliar_usuario.html", {"form": form, "usuario": usuario_avaliado})

# ------------------------------
# Home
# ------------------------------
def home(request):
    # Pega as 5 caronas mais recentes
    caronas_recentes = Carona.objects.all().order_by('-criado_em')[:5]
    return render(request, "home.html", {"caronas_recentes": caronas_recentes})
