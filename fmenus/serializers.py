from rest_framework import serializers

from .models import MenuItem


class MenuItemSerializer(serializers.ModelSerializer):
    has_submenu = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem

    def get_has_submenu(self, obj):
        return obj.has_submenu
