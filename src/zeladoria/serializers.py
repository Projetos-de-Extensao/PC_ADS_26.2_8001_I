from rest_framework import serializers
from .models import *

class UnidadeSerializer(serializers.ModelSerializer):
    class Meta: model=UnidadeAtendimento; fields="__all__"; read_only_fields=("id","codigo","criado_em")

class SolicitacaoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=SolicitacaoZeladoria
        fields=("id","protocolo","servico","descricao","respostas_adicionais","formulario_versao","logradouro","numero","complemento","bairro","cep","ponto_referencia","latitude","longitude","criado_em","status")
        read_only_fields=("id","protocolo","criado_em","status")
    def validate_servico(self,v):
        if not v.ativo or not v.assunto.ativo or not v.assunto.tema.ativo or not v.assunto.tema.modulo.ativo: raise serializers.ValidationError("Serviço indisponível.")
        return v
    def validate_cep(self,v):
        v=v.replace("-","").strip()
        if v and (len(v)!=8 or not v.isdigit()): raise serializers.ValidationError("CEP deve conter 8 dígitos.")
        return v
    def validate(self,a):
        lat,lon=a.get("latitude"),a.get("longitude")
        if (lat is None)!=(lon is None): raise serializers.ValidationError("Latitude e longitude devem ser informadas juntas.")
        if lat is not None and not -90<=lat<=90: raise serializers.ValidationError({"latitude":"Fora do intervalo válido."})
        if lon is not None and not -180<=lon<=180: raise serializers.ValidationError({"longitude":"Fora do intervalo válido."})
        return a
    
class ServicoResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicoCatalogo
        fields = ("id", "codigo", "nome", "descricao")


class UnidadeResumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeAtendimento
        fields = ("id", "codigo", "nome")

class SolicitacaoReadSerializer(serializers.ModelSerializer):
    solicitante = serializers.StringRelatedField(read_only=True)
    servico = ServicoResumoSerializer(read_only=True)
    unidade_atual = UnidadeResumoSerializer(read_only=True)

    servico_detalhe = ServicoResumoSerializer(
        source="servico", read_only=True
    )

    unidade_atual_detalhe = UnidadeResumoSerializer(
        source="unidade_atual", read_only=True
    )

    class Meta:
        model = SolicitacaoZeladoria
        fields = (
            "id", "protocolo", "solicitante",
            "servico", "unidade_atual",
            "descricao", "respostas_adicionais",
            "formulario_versao", "status",
            "logradouro", "numero", "complemento",
            "bairro", "cep", "ponto_referencia",
            "latitude", "longitude",
            "criado_em", "atualizado_em",
            "servico_detalhe", "unidade_atual_detalhe"
        )
        
class HistoricoSerializer(serializers.ModelSerializer):
    class Meta: model=HistoricoSolicitacao; fields="__all__"
class AnexoSerializer(serializers.ModelSerializer):
    enviado_por=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=AnexoSolicitacao
        fields=("id","arquivo","nome_original","tipo_conteudo","tamanho_bytes","enviado_por","criado_em")
        read_only_fields=("id","nome_original","tipo_conteudo","tamanho_bytes","enviado_por","criado_em")
    def validate_arquivo(self,f):
        if f.size>5*1024*1024: raise serializers.ValidationError("Limite de 5 MB.")
        if f.content_type not in ("image/jpeg","image/png","image/webp"): raise serializers.ValidationError("Formato permitido: JPEG, PNG ou WEBP.")
        return f
    def create(self,data):
        f=data["arquivo"]; u=self.context["request"].user
        data.update(enviado_por=u,nome_original=f.name[:255],tipo_conteudo=getattr(f,"content_type",""),tamanho_bytes=f.size)
        return super().create(data)

class SolicitacaoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=SolicitacaoZeladoria
        fields=("descricao","respostas_adicionais","unidade_atual","responsavel")
