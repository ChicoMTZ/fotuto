from rest_framework import serializers
from rest_framework.reverse import reverse as drf_reverse

from vars.serializers import VarSerializer
from .models import Mimic, Rule


class MimicPostSerializer(serializers.ModelSerializer):
    # vars = serializers.PrimaryKeyRelatedField(many=True, queryset=Var.objects.all())

    class Meta:
        model = Mimic
        exclude = ('vars',)


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule


class MimicSerializer(serializers.ModelSerializer):
    vars = VarSerializer(many=True, read_only=True)
    rules = RuleSerializer(many=True, read_only=True)
    graphic = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = Mimic

    def get_graphic(self, obj):
        return obj.render_graphic().replace('&#39;', "'")

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': drf_reverse('mimic-detail', kwargs={'pk': obj.pk}, request=request),
            'window': drf_reverse('window-detail', kwargs={'pk': obj.window.pk}, request=request),
            'vars': drf_reverse('var-list', request=request) + '?mimic=%s' % format(obj.pk),
            'rules': drf_reverse('rule-list', request=request) + '?mimic=%s' % format(obj.pk),
        }
