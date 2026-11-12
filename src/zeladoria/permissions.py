from rest_framework.permissions import BasePermission
def servidor(user):
    return user.is_authenticated and (user.is_staff or user.tipo=="SERVIDOR" or user.groups.filter(name="Servidor").exists())
class SolicitacaoPermission(BasePermission):
    def has_permission(self,request,view): return request.user.is_authenticated
    def has_object_permission(self,request,view,obj): return servidor(request.user) or obj.solicitante_id==request.user.id
