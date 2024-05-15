from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Entreprise, Service, CustomUser,Team
from .serializers import  EntrepriseSerializer, TeamSerializer, ServiceSerializer, UserSerializer
# Create your views here.

class EntrepriseSuperUserView(viewsets.ModelViewSet):
    queryset= Entreprise.objects.all()
    serializer_class = EntrepriseSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        entreprise = self.get_object()
        entreprise.is_active = not entreprise.is_active
        entreprise.save()
        msg={
            'message': 'Entreprise activer/desactiver avec succes'
        }
        return Response(msg, status=status.HTTP_200_OK)

class EntrepriseAdminView(viewsets.ModelViewSet):
    queryset= Entreprise.objects.all()
    serializer_class = EntrepriseSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['delete'], detail=True)
    def delete(self, request, *args, **kwargs):
        msg={
            'message' : 'Vous ne pouvez pas supprimer cette entreprise'
        }
        return Response(msg, status=status.HTTP_401_UNAUTHORIZED)
    
     

class ServiceView(viewsets.ModelViewSet):
    queryset= Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['delete'], detail=True)
    def delete(self, request, *args, **kwargs):
        msg={
            'message' : 'Vous ne pouvez pas supprimer ce service'
        }
        return Response(msg, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None):
        team= self.get_object()
        team.is_active = not team.is_active
        team.save()
        msg={
            'message': 'Service activer/desactiver avec succes'
        }
        return Response(msg, status=status.HTTP_200_OK)

class TeamView(viewsets.ModelViewSet):
    queryset= Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None):
        team= self.get_object()
        team.is_active = not team.is_active
        team.save()
        msg={
            'message': 'Team activer/desactiver avec succes'
        }
        return Response(msg, status=status.HTTP_200_OK)
    
class UserView(viewsets.ModelViewSet):
    queryset= CustomUser.objects.all()
    serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

