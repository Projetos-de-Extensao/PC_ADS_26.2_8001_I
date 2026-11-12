from rest_framework import serializers
from django.contrib.auth import get_user_model
User=get_user_model()
class CadastroSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,min_length=8)
    class Meta:
        model=User
        fields=("id","username","email","cpf","password")
        read_only_fields=("id",)
    def create(self,validated_data): return User.objects.create_user(**validated_data)
