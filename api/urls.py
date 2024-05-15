from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import  ServiceView, EntrepriseSuperUserView, TeamView, UserView
# , UserView
# ,EntrepriseAdminView

router = DefaultRouter()

router.register('team',TeamView)
router.register('entrepriseSuperUser',EntrepriseSuperUserView)
router.register('user',UserView)
router.register('service',ServiceView)



urlpatterns = [
    path('', include(router.urls)),
]
