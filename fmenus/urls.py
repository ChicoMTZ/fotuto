from django.conf.urls import url, include
from rest_framework import routers

from .views import MenuItemViewSet

router = routers.DefaultRouter()
router.register(r'menus', MenuItemViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]