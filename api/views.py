from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Entreprise, Service, CustomUser,Team
from .serializers import  EntrepriseSerializer, TeamSerializer, ServiceSerializer, UserSerializer
# Create your views here.

class EntrepriseView(viewsets.ModelViewSet):
    queryset= Entreprise.objects.all()
    serializer_class = EntrepriseSerializer
    permission_classes = [IsAuthenticated]

    def list(self,request):
        user= request.user
        # print("ID de rôle de l'utilisateur :", user.roleId.name)
        if user.roleId.name == 'superuser':
            entreprise = Entreprise.objects.all()
            serializer = EntrepriseSerializer(entreprise, many=True)
            msg={
                'message': 'Voici la liste',
                'resultat' : serializer.data
            }
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg={
                'message': 'Vous n avez pas le droit d acceder a la liste des entreprises'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)
        
    def retrieve(self,request,pk=None):
        user= request.user
        if user.roleId.name == 'superuser' or user.roleId.name == 'admin':
            entreprise = Entreprise.objects.get(pk=pk)
            serializer = EntrepriseSerializer(entreprise, many=True)
            msg={
                'message': 'Voici les info ce cette entreprise',
                'resultat' : serializer.data
            }
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg={
                'message': 'Vous n\'avez pas le droit d\'acceder a cette page'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user= request.user
        if user.roleId.name == 'superuser':
            entreprise = self.get_object()
            entreprise.is_active = not entreprise.is_active
            entreprise.save()
            msg={
                'message': 'Entreprise activer/desactiver avec succes'
            }
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg={
                'message': 'Vous n aveez pas le droit d activation/desactivation'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, *args, **kwargs):
        msg={
            'message' : 'Vous ne pouvez pas supprimer cette entreprise'
        }
        return Response(msg, status=status.HTTP_401_UNAUTHORIZED)

    def create(self,request):
        user = request.user
        if user.roleId.name == 'admin':
            entreprise= Entreprise.objects.create(**request.data)  
            serializer = EntrepriseSerializer(entreprise)
            # serializer.is_valid(raise_exception=True)
            # self.perform_create(serializer)
            msg={
                'message' : 'Entreprise creer avec succees',
                'resultat' : serializer.data
            }
            return Response(msg, status=status.HTTP_201_CREATED)
        else:
            msg={
                'message': 'Vous n aveez pas le droit de creer une entreprise'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)

    def update(self,request,pk=None):
        user = request.user
        if user.roleId.name == 'admin':
            try:
                entreprise= Entreprise.objects.get(pk=pk)  
            except Entreprise.DoesNotExists:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = EntrepriseSerializer(entreprise, data=request.data)
            if serializer.is_valid():
                serializer.save()
                msg={
                'message' : 'Entreprise modifier avec succees',
                'resultat' : serializer.data
                }
                return Response(msg)
            return Response(status=status.HTTP_400_BAD_REQUEST)   
        else:
            msg={
                'message': 'Vous n aveez pas le droit de modifier une entreprise'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)


class ServiceView(viewsets.ModelViewSet):
    queryset= Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self,request,pk=None):
        user= request.user
        if user.roleId.name == 'admin':
            
            service = Service.objects.get(pk=pk)
            serializer = ServiceSerializer(service)
            print('--avant msg---')
            msg={
                'message': 'Voici les info de ce service',
                'resultat' : serializer.data
            }
            print('--apres msg---')
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg={
                'message': 'Vous n\'avez pas le droit d\'acceder a cette page'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)     

    def list(self,request):
        user= request.user
        if user.roleId.name == 'admin':
            service = Service.objects.all()
            serializer = ServiceSerializer(service, many=True)
            msg={
                'message': 'Voici la liste',
                'resultat' : serializer.data
            }
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg={
                'message': 'Vous n\'avez pas le droit d acceder a la liste des services'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        msg={
            'message' : 'Vous ne pouvez pas supprimer cette entreprise'
        }
        return Response(msg, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.roleId.name == 'admin':
            entreprise_id = request.data.get('entreprise')
            try:
                entreprise = Entreprise.objects.get(pk=entreprise_id)
            except Entreprise.DoesNotExist:
                msg = {
                    'message': 'L\'entreprise spécifiée n\'existe pas'
                }
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            
            request.data['entreprise'] = entreprise_id  #
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            msg = {
                'message': 'Service crée avec succees',
                'resultat' : serializer.data
            }
            return Response(msg, status=status.HTTP_201_CREATED)
        else:
            msg = {
                'message': 'Vous n\'avez pas le droit de créer un service'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)

    def update(self,request,pk=None):
        user = request.user
        if user.roleId.name == 'admin':
            try:
                service= Service.objects.get(pk=pk)  
            except Team.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            
            entreprise_id = request.data.get('entreprise')
            try:
                entreprise = Entreprise.objects.get(pk=entreprise_id)
            except Entreprise.DoesNotExist:
                msg={
                    'message': 'L\'entreprise spécifiée n\'existe pas'
                    }
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            serializer = ServiceSerializer(service, data=request.data)
            if serializer.is_valid():
                serializer.save()
                msg={
                'message' : 'Service modifier avec succees',
                'resultat' : serializer.data
                }
                return Response(msg)
            return Response(status=status.HTTP_400_BAD_REQUEST)   
        else:
            msg={
                'message': 'Vous n\'avez pas le droit de modifier un service'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None):
        user= request.user
        if user.roleId.name == 'admin':
            team= self.get_object()
            team.is_active = not team.is_active
            team.save()
            msg={
                'message': 'Service activer/desactiver avec succes'
            }
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg={
                'message': 'Vous n aveez pas le droit d activation/desactivation'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)

class TeamView(viewsets.ModelViewSet):
    queryset= Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.roleId.name == 'admin':
            entreprise_id = request.data.get('entreprise')
            try:
                entreprise = Entreprise.objects.get(pk=entreprise_id)
            except Entreprise.DoesNotExist:
                msg = {
                    'message': 'L\'entreprise spécifiée n\'existe pas'
                }
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            
            # Créez une équipe en utilisant l'ID de l'entreprise
            request.data['entreprise'] = entreprise_id  # Ajout de l'ID de l'entreprise aux données de la requête
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            msg = {
                'message': 'Team créer avec succees',
                'resultat' : serializer.data
            }
            return Response(msg, status=status.HTTP_201_CREATED)
        else:
            msg = {
                'message': 'Vous n\'avez pas le droit de créer une team'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)

    def list(self,request):
        user= request.user
        if user.roleId.name == 'admin':
            team = Team.objects.all()
            serializer = TeamSerializer(team, many=True)
            msg={
                'message': 'Voici la liste',
                'resultat' : serializer.data
            }
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg={
                'message': 'Vous n\'avez pas le droit d\'acceder a la liste des teams'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)

    # @action(methods=['get'], detail=True)
    def retrieve(self,request,pk=None):
        user= request.user
        if  user.roleId.name == 'admin':
            team = Team.objects.get(pk=pk)
            serializer = TeamSerializer(team)
            msg={
                'message': 'Voici les info de cette team',
                'resultat' : serializer.data
            }
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg={
                'message': 'Vous n\'avez pas le droit d\'acceder a cette page'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)
    
    def update(self,request,pk=None):
        user = request.user
        if user.roleId.name == 'admin':
            try:
                team= Team.objects.get(pk=pk)  
            except Team.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            
            entreprise_id = request.data.get('entreprise')
            try:
                entreprise = Entreprise.objects.get(pk=entreprise_id)
            except Entreprise.DoesNotExist:
                msg={
                    'message': 'L\'entreprise spécifiée n\'existe pas'
                    }
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            serializer = TeamSerializer(team, data=request.data)
            if serializer.is_valid():
                serializer.save()
                msg={
                'message' : 'Team modifier avec succees',
                'resultat' : serializer.data
                }
                return Response(msg)
            return Response(status=status.HTTP_400_BAD_REQUEST)   
        else:
            msg={
                'message': 'Vous n aveez pas le droit de modifier un team'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)

    
        user = request.user
        if user.roleId.name == 'admin':
            try:
                team = Team.objects.get(pk=pk)  
            except Team.DoesNotExist:
                msg={
                    'message' : 'Team n\'est pas trouve',
                }
                return Response(status=status.HTTP_404_NOT_FOUND)
            team.delete()
            msg={
                'message' : 'Team supprimer avec succees',
            }
            return Response(msg, status=status.HTTP_204_NO_CONTENT) 
        else:
            msg={
                'message': 'Vous n avez pas le droit de supprimer un team'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)  
   
    def destroy(self, request, pk=None):
        user = request.user
        if user.roleId.name == 'admin':
            try:
                team = Team.objects.get(pk=pk)
                team.delete()
                return Response({'message': 'Team supprimée avec succès'}, status=status.HTTP_200_OK)
            except Team.DoesNotExist:
                return Response({'message': 'Team n\'est pas trouvée'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Vous n\'avez pas le droit de supprimer un team'}, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['post'], detail=True)
    def activate(self, request, pk=None):
        user= request.user
        if user.roleId.name == 'admin':
            team= self.get_object()
            team.is_active = not team.is_active
            team.save()
            msg={
                'message': 'Team activer/desactiver avec succes'
            }
            return Response(msg, status=status.HTTP_200_OK)
        else:
            msg={
                'message': 'Vous n aveez pas le droit d activation/desactivation'
            }
            return Response(msg, status=status.HTTP_403_FORBIDDEN)
    
