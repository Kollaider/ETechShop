from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api.views import NetworkNodeViewSet


router = routers.DefaultRouter()
router.register(r'networknodes', NetworkNodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', obtain_auth_token, name='api_token_auth'),
]

urlpatterns += router.urls
