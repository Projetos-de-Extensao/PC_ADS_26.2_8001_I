from django.db import models
from django.contrib.postgres.indexes import GinIndex
class CodigoAutomatico(models.Model):
    codigo=models.CharField(max_length=20,unique=True,editable=False)
    class Meta: abstract=True
    def save(self,*args,**kwargs):
        if not self.codigo:
            prefix=self.__class__.__name__[:3].upper()
            last=self.__class__.objects.order_by("-id").first()
            self.codigo=f"{prefix}{(last.id if last else 0)+1:06d}"
        super().save(*args,**kwargs)
class ModuloPortal(CodigoAutomatico):
    nome=models.CharField(max_length=150); descricao=models.TextField(blank=True,default="")
    ativo=models.BooleanField(default=True); ordem=models.PositiveIntegerField(default=0)
    criado_em=models.DateTimeField(auto_now_add=True); atualizado_em=models.DateTimeField(auto_now=True)
    class Meta: ordering=["ordem","nome"]
    def __str__(self): return self.nome
class Tema(CodigoAutomatico):
    modulo=models.ForeignKey(ModuloPortal,on_delete=models.PROTECT,related_name="temas")
    nome=models.CharField(max_length=150); descricao=models.TextField(blank=True,default="")
    ativo=models.BooleanField(default=True); ordem=models.PositiveIntegerField(default=0)
    class Meta: ordering=["ordem","nome"]
    def __str__(self): return self.nome
class Assunto(CodigoAutomatico):
    tema=models.ForeignKey(Tema,on_delete=models.PROTECT,related_name="assuntos")
    nome=models.CharField(max_length=150); descricao=models.TextField(blank=True,default="")
    ativo=models.BooleanField(default=True); ordem=models.PositiveIntegerField(default=0)
    class Meta: ordering=["ordem","nome"]
    def __str__(self): return self.nome
class ServicoCatalogo(CodigoAutomatico):
    assunto=models.ForeignKey(Assunto,on_delete=models.PROTECT,related_name="servicos")
    nome=models.CharField(max_length=200); descricao=models.TextField()
    instrucoes=models.TextField(blank=True,default=""); prazo_estimado_dias=models.PositiveIntegerField(null=True,blank=True)
    formulario_config=models.JSONField(default=dict,blank=True); versao_formulario=models.PositiveIntegerField(default=1)
    ativo=models.BooleanField(default=True); ordem=models.PositiveIntegerField(default=0)
    criado_em=models.DateTimeField(auto_now_add=True); atualizado_em=models.DateTimeField(auto_now=True)
    class Meta:
        ordering=["ordem","nome"]
        indexes=[GinIndex(fields=["formulario_config"],name="serv_form_cfg_gin")]
    def __str__(self): return self.nome
