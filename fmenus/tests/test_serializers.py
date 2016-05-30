from unittest import TestCase
from rest_framework.test import APIRequestFactory

from fmenus.models import MenuItem
from fmenus.serializers import MenuItemSerializer


class MenuItemSerializerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(MenuItemSerializerTestCase, cls).setUpClass()
        cls.factory = APIRequestFactory()

    def setUp(self):
        super(MenuItemSerializerTestCase, self).setUp()
        self.menu_1_data = {'position': 'view', 'text': 'Menu 1', 'link': '#/menu'}
        self.menu_1 = MenuItem.objects.create()

    def test_validate(self):
        serializer = MenuItemSerializer(
            data=self.menu_1_data,
            context={'request': self.factory.get('/api/menus/')}
        )
        valid = serializer.is_valid()
        self.assertTrue(valid, serializer.errors)
        serializer.save()
        # TODO: self.assertEqual(serializer.data)
