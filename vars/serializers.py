from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.reverse import reverse as drf_reverse
from .models import Device, Var


class VarSerializer(serializers.ModelSerializer):
    var_type_display = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = Var
        read_only_fields = ('slug', 'var_type_display')

    def validate(self, data):
        # TODO: This logic should reside in model save method
        name_slug = slugify(data['name'])
        data['slug'] = name_slug
        i = 1
        while Var.objects.filter(slug=data['slug']).count() > 0:
            data['slug'] = '{}-{}'.format(name_slug, i)
            i += 1
        return data

    def get_var_type_display(self, obj):
        return obj.get_var_type_display()

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': drf_reverse('var-detail', kwargs={'pk': obj.pk}, request=request),
            'device': drf_reverse('device-detail', kwargs={'pk': obj.device.pk}, request=request),
        }


class DevicePostSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = Device
        read_only_fields = ('slug',)

    def validate(self, data):
        # TODO: This logic should reside in model save method
        name_slug = slugify(data['name'])
        data['slug'] = name_slug
        i = 1
        while Device.objects.filter(slug=data['slug']).count() > 0:
            data['slug'] = '{}-{}'.format(name_slug, i)
            i += 1
        return data

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': drf_reverse('device-detail', kwargs={'pk': obj.pk}, request=request),
            'vars': drf_reverse('var-list', request=request) + '?device={}'.format(obj.pk),
        }


class DeviceSerializer(serializers.ModelSerializer):
    vars = VarSerializer(many=True)
    links = serializers.SerializerMethodField()

    class Meta:
        model = Device

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': drf_reverse('device-detail', kwargs={'pk': obj.pk}, request=request),
            'vars': drf_reverse('var-list', request=request) + '?device={}'.format(obj.pk),
        }
