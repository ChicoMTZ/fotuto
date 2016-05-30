from unittest import TestCase

from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from windows.serializers import WindowSerializer

User = get_user_model()


class WindowSerializerTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_validate(self):
        """
        Tests that WindowSerializer.validate() adds a slugged
        version of the title attribute to the data
        """
        serializer = WindowSerializer()
        data = serializer.validate({'title': 'A window'})
        self.assertEqual(data, {
            'title': 'A window',
            'slug': 'a-window'
        })

    def test_get_links(self):
        serializer = WindowSerializer(
            data={'title': "Alarm system", 'slug': 'alarm-system'},
            context={'request': self.factory.get('/api/windows/')}
        )
        serializer.is_valid()
        window = serializer.save()
        self.assertDictContainsSubset({'links': {
            'self': 'http://testserver/api/windows/%s/' % window.pk,
            'mimics': 'http://testserver/api/mimics/?window=%s' % window.pk,
            'vars': 'http://testserver/api/vars/?mimic__window=%s' % window.pk,
        }}, serializer.data,)
