from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Carona, Avaliacao

# ------------------------------
# Formulário de Cadastro de Usuário
# ------------------------------
class CadastroForm(UserCreationForm):
    nome = forms.CharField(max_length=100, label='Nome')
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'email', 'password1', 'password2']


# ------------------------------
# Formulário de Edição de Usuário / UsuarioForm
# ------------------------------
class UsuarioForm(forms.ModelForm):
    nome = forms.CharField(max_length=100, label='Nome')
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'email']
        labels = {
            'username': 'Usuário',
        }


# ------------------------------
# Formulário de Login
# ------------------------------
class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')


# ------------------------------
# Formulário de Publicação de Carona
# ------------------------------
class CaronaForm(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Data da Carona'
    )

    class Meta:
        model = Carona
        fields = ['origem', 'destino', 'data', 'vagas']
        labels = {
            'origem': 'Origem',
            'destino': 'Destino',
            'vagas': 'Número de Vagas'
        }


# ------------------------------
# Formulário de Avaliação de Usuário
# ------------------------------
class AvaliacaoForm(forms.ModelForm):
    nota = forms.IntegerField(
        min_value=1, 
        max_value=5, 
        label='Nota (1 a 5)',
        widget=forms.NumberInput(attrs={'type': 'number'})
    )

    comentario = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Comentário'
    )

    class Meta:
        model = Avaliacao
        fields = ['comentario', 'nota']


# ------------------------------
# Formulário de Busca de Caronas
# ------------------------------
class BuscarCaronaForm(forms.Form):
    destino = forms.CharField(required=False, label='Destino')
    data = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Data'
    )
