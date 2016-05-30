from unittest import TestCase
from rest_framework.test import APIRequestFactory

from mimics.models import Mimic
from mimics.serializers import MimicSerializer, MimicPostSerializer
from vars.models import Device, Var
from windows.models import Window


class MimicSerializerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(MimicSerializerTestCase, cls).setUpClass()
        cls.factory = APIRequestFactory()
        cls.window = Window.objects.create(title="Security System", slug='security-system')
        cls.device = Device.objects.create(name="Door sensor")
        cls.var_door_state = Var.objects.create(name="Door State", slug="door_state", device=cls.device)

    def test_create_allow_to_specify_vars(self):
        """Vars should contains vars data instead of links to avoid n+1 problem"""
        # TODO: Fix this
        serializer = MimicPostSerializer(
            data={
                'name': "Alarm Controller 1",
                'slug': 'alarm-controller-1',
                'window': self.window.pk,
                # 'vars': [self.var_door_state.pk]
            },
            context={'request': self.factory.get('/api/mimics/')}
        )
        valid = serializer.is_valid()
        self.assertTrue(valid, serializer.errors)
        serializer.save()
        # self.assertEqual(serializer.data['vars'][0], self.var_door_state.pk)

    def test_get_links(self):
        # TODO: `Mimic.window` field should not be required, in fact, `mimics` can creates as a library to select from
        #     it to use in `Windows`, so there should be a m2m field `windows.mimics` instead `mimic.window`
        serializer = MimicSerializer(
            data={'name': "Alarm Controller", 'slug': 'alarm-controller', 'window': self.window.pk, 'vars': [], 'rules': []},
            context={'request': self.factory.get('/api/mimics/')}
        )
        valid = serializer.is_valid()
        self.assertTrue(valid, serializer.errors)
        mimic = serializer.save()
        self.assertDictContainsSubset({
            'links': {
                'self': 'http://testserver/api/mimics/%s/' % mimic.pk,
                'window': 'http://testserver/api/windows/%s/' % mimic.window.pk,
                'vars': 'http://testserver/api/vars/?mimic=%s' % mimic.pk,
                'rules': 'http://testserver/api/rules/?mimic=%s' % mimic.pk,
            }
        }, serializer.data)

    def test_graphic_is_rendered(self):
        graphic = '<rect width="{{ door_state }}">'
        expected_graphic = """<rect width="{{ (mimic.vars | getItem:'door_state').value }}">"""
        mimic_data = {'name': "GPS", 'window': self.window, 'graphic': graphic}
        mimic = Mimic.objects.create(**mimic_data)
        # Add vars
        mimic.vars.add(self.var_door_state)
        serializer = MimicSerializer(mimic, context={'request': self.factory.get('/api/mimics/%s/' % mimic.pk)})
        self.assertEqual(serializer.data.get('graphic'), expected_graphic)
