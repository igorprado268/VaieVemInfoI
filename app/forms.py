from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Carona, Avaliacao
from datetime import datetime

# ------------------------------
# Formulário de Cadastro de Usuário
# ------------------------------
class CadastroForm(UserCreationForm):
    TIPO_CAMPUS_CHOICES = [
        ('inconfidentes', 'INCONFIDENTES'),
        ('machado', 'MACHADO'),
        ('muzambinho', 'MUZAMBINHO'),
        ('passos', 'PASSOS'),
        ('pouso alegre', 'POUSO ALEGRE'),
        ('poços de caldas', 'POÇOS DE CALDAS'),
        ('três corações', 'TRÊS CORAÇÕES'),
    ]
    nome = forms.CharField(max_length=100, required=True, label="Nome")
    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=15, required=False)
    campus = forms.ChoiceField(choices=TIPO_CAMPUS_CHOICES, label="Campus")


    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'telefone', 'campus']
 
    def save(self, commit=True):
        user = super().save(commit=False)
        user.nome = self.cleaned_data["nome"]
        user.email = self.cleaned_data["email"]
        user.telefone = self.cleaned_data.get("telefone", "")
        user.campus = self.cleaned_data["campus"]
        
        # Gera username a partir do email (parte antes do @)
        user.username = self.cleaned_data["email"].split('@')[0]
        
        # Garante que o username seja único
        base_username = user.username
        counter = 1
        while Usuario.objects.filter(username=user.username).exists():
            user.username = f"{base_username}{counter}"
            counter += 1
        
        if commit:
            user.save()
        return user

# ------------------------------
# Formulário de Edição de Usuário
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
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Hora da Carona'
    )

    class Meta:
        model = Carona
        fields = ['origem', 'destino', 'data', 'hora', 'vagas']
        labels = {
            'origem': 'Origem',
            'destino': 'Destino',
            'vagas': 'Número de Vagas'
        }

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data')
        hora = cleaned_data.get('hora')
        if data and hora:
            cleaned_data['data'] = datetime.combine(data, hora)
        return cleaned_data


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
        required=False,
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
    origem = forms.CharField(required=False, label='Origem')
    destino = forms.CharField(required=False, label='Destino')
    data = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Data'
    )
