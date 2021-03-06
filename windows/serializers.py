from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.reverse import reverse as drf_reverse

from .models import Window


class WindowSerializer(serializers.ModelSerializer):
    mimics = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='mimic-detail')
    links = serializers.SerializerMethodField()

    class Meta:
        model = Window
        read_only_fields = ('slug',)

    def validate(self, data):
        data['slug'] = slugify(data['title'])
        return data

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': drf_reverse('window-detail', kwargs={'pk': obj.pk}, request=request),
            'mimics': drf_reverse('mimic-list', request=request) + '?window={}'.format(obj.pk),
            'vars': drf_reverse('var-list', request=request) + '?mimic__window={}'.format(obj.pk),
        }
