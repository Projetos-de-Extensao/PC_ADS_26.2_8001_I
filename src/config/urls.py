from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from usuarios.views import CadastroView
from catalogo.views import ModuloViewSet, TemaViewSet, AssuntoViewSet, ServicoViewSet
from zeladoria.views import UnidadeViewSet, SolicitacaoViewSet
r=DefaultRouter()
r.register("modulos",ModuloViewSet); r.register("temas",TemaViewSet); r.register("assuntos",AssuntoViewSet)
r.register("servicos",ServicoViewSet); r.register("unidades",UnidadeViewSet); r.register("solicitacoes",SolicitacaoViewSet,basename="solicitacao")
urlpatterns=[
 path("admin/",admin.site.urls), path("api/auth/cadastro/",CadastroView.as_view()),
 path("api/auth/token/",TokenObtainPairView.as_view()), path("api/auth/token/refresh/",TokenRefreshView.as_view()),
 path("api/",include(r.urls)), path("api/schema/",SpectacularAPIView.as_view()),
 path("api/docs/",SpectacularSwaggerView.as_view(url_name="schema")),
]
