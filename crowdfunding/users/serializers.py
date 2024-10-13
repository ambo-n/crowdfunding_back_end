from rest_framework import serializers
from .models import CustomUser
from projects .serializers import ProjectSerializer

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password':{'write_only': True}}
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class CustomUserDetailSerializer(CustomUserSerializer):
    owned_projects = ProjectSerializer(many=True, read_only=True)