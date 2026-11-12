from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import CadastroSerializer
class CadastroView(generics.CreateAPIView):
    serializer_class=CadastroSerializer
    permission_classes=[AllowAny]
