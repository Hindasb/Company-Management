from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
# Create your models here.
entreprisedomain=(
    ('technology','technology' ),
    ('industry','industry')
)
permission_type=(
    ('Read','read'),
    ('Write','write'),
    ('Delete','delete')
)
class Entreprise(models.Model):
    name = models.CharField(max_length=100)
    logo = models.CharField(max_length=100)
    telephone = models.CharField(max_length=50)
    adresse = models.CharField( max_length=150)
    domaine = models.CharField(max_length=50 ,choices=entreprisedomain)
    description = models.CharField(max_length=200)
    Police = models.CharField(max_length=50)
    couleur = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    date_de_creation = models.DateTimeField( auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True) 
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    date_de_creation = models.DateTimeField( auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True)  
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
            return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200)
    date_de_creation = models.DateTimeField( auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name


class CustomPermission(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=50,choices=permission_type)
    roleId = models.ForeignKey(Role, on_delete=models.CASCADE) 
    date_de_creation = models.DateTimeField( auto_now_add=True)
    date_de_modification = models.DateTimeField(auto_now=True) 

    permission = models.OneToOneField(
        Permission,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=100)
    entrepriseId = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True)
    createdBy = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    teamId = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)   
    date_de_modification = models.DateTimeField(auto_now=True)
    roleId = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)   
   

    def save(self, *args, **kwargs):
            if self.roleId and self.roleId.name == 'admin':
                self.is_staff = True
                self.is_superuser = False
            elif self.roleId and self.roleId.name == 'superuser':
                self.is_staff = True
                self.is_superuser = True
            else:
                self.is_staff = False
                self.is_superuser = False 
            super().save(*args, **kwargs)
