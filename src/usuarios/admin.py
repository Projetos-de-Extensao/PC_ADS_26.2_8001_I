from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets=UserAdmin.fieldsets+(("Dados do Portal",{"fields":("cpf","tipo")}),)
    list_display=("username","email","cpf","tipo","is_staff","is_active")
