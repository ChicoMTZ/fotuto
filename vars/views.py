from django import http
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import CreateView
from vars.forms import VarForm, DeviceForm
from vars.models import Var, Device


class DeviceCreateView(SuccessMessageMixin, CreateView):
    model = Device
    form_class = DeviceForm
    success_url = reverse_lazy('device_list')
    success_message = "Device was added."


class VarCreateView(SuccessMessageMixin, CreateView):
    """Add new var"""
    model = Var
    form_class = VarForm
    success_url = reverse_lazy('var_list')
    success_message = "Variable was added."

    def dispatch(self, request, *args, **kwargs):
        if Device.objects.count() == 0:
            messages.info(request, "Please, add a device first.")
            return http.HttpResponseRedirect(reverse('device_add'))
        return super(VarCreateView, self).dispatch(request, *args, **kwargs)
