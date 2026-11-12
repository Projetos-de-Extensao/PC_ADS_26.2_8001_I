from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import SAFE_METHODS,BasePermission
from .models import ModuloPortal,Tema,Assunto,ServicoCatalogo
from .serializers import ModuloSerializer,TemaSerializer,AssuntoSerializer,ServicoSerializer
class LeituraPublicaEscritaStaff(BasePermission):
    def has_permission(self,request,view):
        return request.method in SAFE_METHODS or (request.user.is_authenticated and request.user.is_staff)
class ModuloViewSet(ModelViewSet):
    queryset=ModuloPortal.objects.all(); serializer_class=ModuloSerializer; permission_classes=[LeituraPublicaEscritaStaff]
    search_fields=["nome","descricao","codigo"]; filterset_fields=["ativo"]; ordering_fields=["nome","ordem"]
class TemaViewSet(ModelViewSet):
    queryset=Tema.objects.select_related("modulo").all(); serializer_class=TemaSerializer; permission_classes=[LeituraPublicaEscritaStaff]
    search_fields=["nome","codigo"]; filterset_fields=["ativo","modulo"]; ordering_fields=["nome","ordem"]
class AssuntoViewSet(ModelViewSet):
    queryset=Assunto.objects.select_related("tema","tema__modulo").all(); serializer_class=AssuntoSerializer; permission_classes=[LeituraPublicaEscritaStaff]
    search_fields=["nome","codigo"]; filterset_fields=["ativo","tema"]; ordering_fields=["nome","ordem"]
class ServicoViewSet(ModelViewSet):
    queryset=ServicoCatalogo.objects.select_related("assunto","assunto__tema","assunto__tema__modulo").all()
    serializer_class=ServicoSerializer; permission_classes=[LeituraPublicaEscritaStaff]
    search_fields=["nome","descricao","codigo"]; filterset_fields=["ativo","assunto"]; ordering_fields=["nome","ordem","prazo_estimado_dias"]
