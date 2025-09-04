from django.contrib import admin
from .models import Usuario, Carona, Avaliacao

# ------------------------------
# Registro do Usuário no admin
# ------------------------------
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id_usuario", "username", "nome", "email", "is_staff", "is_active")
    search_fields = ("nome", "email", "username")
    list_filter = ("is_staff", "is_active")
    ordering = ("id_usuario",)


# ------------------------------
# Registro da Carona no admin
# ------------------------------
@admin.register(Carona)
class CaronaAdmin(admin.ModelAdmin):
    list_display = ("id_carona", "usuario", "origem", "destino", "data", "vagas")
    search_fields = ("origem", "destino", "usuario__username")
    list_filter = ("data", "origem", "destino")
    ordering = ("data",)


# ------------------------------
# Registro da Avaliação no admin
# ------------------------------
@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("id_avaliacao", "avaliador", "avaliado", "nota", "comentario")
    search_fields = ("comentario", "avaliador__username", "avaliado__username")
    list_filter = ("nota",)
    ordering = ("id_avaliacao",)
