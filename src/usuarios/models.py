from django.contrib.auth.models import AbstractUser
from django.db import models
class Usuario(AbstractUser):
    class Tipo(models.TextChoices):
        CIDADAO="CIDADAO","Cidadão"
        SERVIDOR="SERVIDOR","Servidor"
    email=models.EmailField(unique=True)
    cpf=models.CharField(max_length=11,unique=True,null=True,blank=True)
    tipo=models.CharField(max_length=12,choices=Tipo.choices,default=Tipo.CIDADAO)
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["username"]
    def __str__(self): return self.email
