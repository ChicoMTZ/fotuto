from importlib import import_module

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.utils.text import slugify
from django.views.generic.base import TemplateView
from rest_framework.authtoken import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse as drf_reverse

try:
    from settings_local import ADDITIONAL_APPS
except ImportError:
    ADDITIONAL_APPS = []

admin.site.site_title = "Fotuto Admin Site"
admin.site.site_header = "Fotuto administration"
admin.site.index_title = "Fotuto administration"

@api_view(['GET'])
def api_root(request, format=None):
    # TODO: Add endpoints from addons
    return Response({
        'windows': drf_reverse('window-list', request=request, format=format),
        'devices': drf_reverse('device-list', request=request, format=format),
        'users': drf_reverse('user-list', request=request, format=format),
        'menus': drf_reverse('menuitem-list', request=request, format=format),
    })

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='spa/index.html'), {'addons': ADDITIONAL_APPS}),
    url(r'^api/$', api_root),
    url(r'^api/token/', views.obtain_auth_token, name='api-token'),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include('operators.urls')),
    url(r'^', include('windows.urls')),
    url(r'^', include('mimics.urls')),
    url(r'^', include('vars.urls')),
    url(r'^', include('fmenus.urls')),
    url(r'^admin/', include(admin.site.urls)),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Dynamically add urls from extensions
# TODO: Add a unittest for this
for app in ADDITIONAL_APPS:
    # TODO: check it hasn't included yet
    url_module = '{}.urls'.format(app)
    try:
        import_module(url_module)
        # possibly cleanup the after the imported module?
        # might fuss up the `include(...)` or leave a polluted namespace
    except Exception as e:
        # cleanup after module import if fails,
        #  maybe you can let the `include(...)` report failures
        print e
    else:
        url_regex = r'^add-on/{}/'.format(slugify(app))
        urlpatterns += [url(url_regex, include(url_module, app_name=app, namespace=app))]
