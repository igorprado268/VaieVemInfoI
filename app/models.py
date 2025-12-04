from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

class Usuario(AbstractUser):
    nome = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    campus = models.CharField(max_length=50, blank=True, null=True)
    # Define email como campo de autenticação
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username ainda é necessário mas não para login

    
    def __str__(self):
        return self.email


# ------------------------------
# Carona
# ------------------------------
class Carona(models.Model):
    id_carona = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="caronas"
    )
    origem = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    data = models.DateTimeField()
    vagas = models.PositiveIntegerField()
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(default=timezone.now)
    ativa = models.BooleanField(default=True)
    excluida = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.origem} → {self.destino} ({self.data.strftime('%d/%m/%Y %H:%M')})"


# ------------------------------
# Avaliação (usuário avalia outro usuário)
# ------------------------------
class Avaliacao(models.Model):
    id_avaliacao = models.AutoField(primary_key=True)
    avaliador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="avaliacoes_feitas"
    )
    avaliado = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="avaliacoes_recebidas"
    )
    comentario = models.TextField(blank=True, null=True)
    nota = models.PositiveIntegerField()  # 1 a 5 estrelas
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Avaliação {self.nota} de {self.avaliador.nome} para {self.avaliado.nome}"


# ------------------------------
# Solicitação de Vaga
# ------------------------------
class SolicitacaoVaga(models.Model):
    id_solicitacao = models.AutoField(primary_key=True)
    carona = models.ForeignKey(
        Carona,
        on_delete=models.CASCADE,
        related_name="solicitacoes"
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="solicitacoes"
    )
    status_choices = [
        ('pendente', 'Pendente'),
        ('aceita', 'Aceita'),
        ('recusada', 'Recusada'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pendente')
    criado_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario.nome} -> {self.carona.origem} → {self.carona.destino} ({self.status})"


# ------------------------------
# Histórico de Avaliações por Carona (opcional)
# ------------------------------
class HistoricoAvaliacao(models.Model):
    id_historico = models.AutoField(primary_key=True)
    carona = models.ForeignKey(Carona, on_delete=models.CASCADE, related_name="historico_avaliacoes")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nota = models.PositiveIntegerField()
    comentario = models.TextField(blank=True, null=True)
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Avaliação {self.nota} para {self.usuario.nome} na carona {self.carona.id_carona}"
