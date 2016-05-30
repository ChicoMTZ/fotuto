from django.conf.urls import url, include
from rest_framework import routers

from .views import WindowViewSet

router = routers.DefaultRouter()
router.register(r'windows', WindowViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls))
]
