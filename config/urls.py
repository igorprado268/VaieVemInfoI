from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    # ------------------------------
    # Django Admin
    # ------------------------------
    path('admin/', admin.site.urls),

    # ------------------------------
    # Páginas principais do app
    # ------------------------------
    path('', views.index, name='index'),
    path('login/', views.login_usuario, name='login'),
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_usuario, name='logout'),

    # ------------------------------
    # Caronas
    # ------------------------------
    path('caronas/', views.lista_caronas, name='lista_caronas'),
    path('caronas/nova/', views.publicar_carona, name='publicar_carona'),
    path('caronas/<int:id_carona>/', views.detalhes_carona, name='detalhes_carona'),
    path('caronas/<int:id_carona>/contato/', views.redirecionar_whatsapp, name='redirecionar_whatsapp'),
    path('caronas/<int:id_carona>/solicitar/', views.solicitar_vaga, name='solicitar_vaga'),

    # ------------------------------
    # Perfil do usuário
    # ------------------------------
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/foto/', views.atualizar_foto, name='atualizar_foto'),
    path('minhas_caronas/', views.minhas_caronas, name='minhas_caronas'),

    # ------------------------------
    # Avaliações
    # ------------------------------
    path('avaliacoes/<int:id_usuario>/', views.avaliar_usuario, name='avaliar_usuario'),
]
