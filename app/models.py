from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

# ------------------------------
# Usuário customizado
# ------------------------------
class Usuario(AbstractUser):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=255)  # Django faz hash da senha automaticamente
    is_admin = models.BooleanField(default=False)

    # Evitar conflito com grupos e permissões do Django
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        help_text="Grupos aos quais este usuário pertence."
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        help_text="Permissões específicas deste usuário."
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome", "username"]  # 'username' ainda é exigido pelo AbstractUser

    def __str__(self):
        return self.nome


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
    nota = models.PositiveIntegerField()  # Ex: 1 a 5 estrelas
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Avaliação {self.nota} de {self.avaliador.nome} para {self.avaliado.nome}"
