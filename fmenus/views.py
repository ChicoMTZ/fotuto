from rest_framework import viewsets

from fmenus.models import MenuItem
from fmenus.serializers import MenuItemSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.filter(active=True)
    serializer_class = MenuItemSerializer
    filter_fields = ('position', 'home')
