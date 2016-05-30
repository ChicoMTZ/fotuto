from rest_framework import viewsets

from .models import Mimic, Rule
from .serializers import MimicSerializer, MimicPostSerializer, RuleSerializer


class MimicViewSet(viewsets.ModelViewSet):
    queryset = Mimic.objects.all()
    filter_fields = ('window',)

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return MimicPostSerializer
        else:
            return MimicSerializer


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    filter_fields = ('var', 'mimic')

