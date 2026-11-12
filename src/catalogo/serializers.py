from rest_framework import serializers
from .models import ModuloPortal,Tema,Assunto,ServicoCatalogo
class ModuloSerializer(serializers.ModelSerializer):
    class Meta: model=ModuloPortal; fields="__all__"; read_only_fields=("id","codigo","criado_em","atualizado_em")
class TemaSerializer(serializers.ModelSerializer):
    class Meta: model=Tema; fields="__all__"; read_only_fields=("id","codigo")
class AssuntoSerializer(serializers.ModelSerializer):
    class Meta: model=Assunto; fields="__all__"; read_only_fields=("id","codigo")
class ServicoSerializer(serializers.ModelSerializer):
    class Meta: model=ServicoCatalogo; fields="__all__"; read_only_fields=("id","codigo","criado_em","atualizado_em")
