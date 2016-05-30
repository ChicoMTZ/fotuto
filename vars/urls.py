from django.conf.urls import include, url
from rest_framework import routers

from vars.views import DeviceViewSet, VarViewSet

router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'vars', VarViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
