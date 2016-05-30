from django.conf.urls import include, url
from rest_framework import routers

from .views import MimicViewSet, RuleViewSet

router = routers.DefaultRouter()
router.register(r'mimics', MimicViewSet)
router.register(r'rules', RuleViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
