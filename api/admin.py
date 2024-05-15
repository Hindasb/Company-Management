from django.contrib import admin
from .models import CustomUser,CustomPermission,Entreprise,Role,Team,Service
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(CustomPermission)
admin.site.register(Entreprise)
admin.site.register(Role)
admin.site.register(Team)
admin.site.register(Service)


admin.site.site_header = 'Company management'
admin.site.site_title = 'Company management'