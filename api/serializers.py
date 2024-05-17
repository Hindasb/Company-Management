from rest_framework import serializers
from .models import Entreprise, Service, Team, Role, CustomUser

class EntrepriseSerializer(serializers.ModelSerializer):
    class Meta():
        model = Entreprise
        fields = '__all__'
        # fields = ['id', 'name', 'logo', 'telephone', 'adresse', 'domaine', 'description', 'police', 'couleur', 'date_de_creation', 'date_de_modification']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta():
        model = Service
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta():
        model = Role
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta():
        model = Team
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = CustomUser
        # fields = ['id', 'entrepriseId', 'roleId', 'createdBy', 'teamId','fullname', 'username', 'password', 'email', 'last_login', 'date_joined', 'date_de_modification']
        fields = '__all__'