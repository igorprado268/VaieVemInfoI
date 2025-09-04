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

    # ------------------------------
    # Caronas
    # ------------------------------
    path('caronas/', views.lista_caronas, name='lista_caronas'),
    path('caronas/nova/', views.publicar_carona, name='publicar_carona'),
    path('caronas/<int:id_carona>/', views.detalhes_carona, name='detalhes_carona'),
    path('caronas/<int:id_carona>/contato/', views.redirecionar_whatsapp, name='redirecionar_whatsapp'),

    # ------------------------------
    # Avaliações
    # ------------------------------
    path('avaliacoes/<int:id_usuario>/', views.avaliar_usuario, name='avaliar_usuario'),
]
