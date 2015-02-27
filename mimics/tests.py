from django.contrib import messages
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase
from fotutils.tests import ModelTestHelper
from mimics.forms import MimicManageForm
from mimics.models import Mimic
from mimics.views import MimicManageView
from windows.models import Window


class MimicModelTest(ModelTestHelper):
    def setUp(self):
        # Mimics require a window
        self.window, create = Window.objects.get_or_create(slug="win1")

    def test_saving_and_retrieving_mimic(self):
        mimic1 = {'name': "First Mimic Name", 'window': self.window}
        mimic2 = {'name': "Second Mimic Name", 'window': self.window}
        # TODO: specify vars
        self.check_saving_and_retrieving_objects(model=Mimic, obj1_dict=mimic1, obj2_dict=mimic2)

    def test_require_window(self):
        self.check_require_field(model=Mimic, required_field='window', error_key='null')


class MimicManagementTest(TestCase):
    maxDiff = None

    def setUp(self):
        # a window is required for a mimic
        self.window, create = Window.objects.get_or_create(slug="win1")
        self.manage_mimic_url = '/windows/%s/mimics/manage/' % self.window.slug

    # TODO: Test add vars in mimic

    def test_add_url_resolves_to_create_view(self):
        found = resolve(self.manage_mimic_url)
        self.assertTrue(found.func, MimicManageView)

    def test_manage_mimic_returns_correct_html(self):
        request = HttpRequest()
        request.method = 'GET'
        generic_add_var_view = MimicManageView()
        generic_add_var_view.request = request
        generic_add_var_view.kwargs = {'window': self.window.slug}
        response = generic_add_var_view.dispatch(request)
        self.assertEqual(response.status_code, 200)
        expected_html = render_to_string('mimics/mimic_manage_form.html', {
            'form': MimicManageForm(initial={'window': self.window.pk}),
            'window': self.window
        })
        self.assertMultiLineEqual(response.rendered_content.decode(), expected_html)

    def test_add_mimic_can_save_a_post_request(self):
        self.client.post(self.manage_mimic_url, data={'window': self.window.pk})
        self.assertEqual(Mimic.objects.count(), 1)
        self.assertEqual(self.window.mimics.count(), 1)
        new_mimic = Mimic.objects.first()
        self.assertEqual(new_mimic.window, self.window)
        self.assertEqual(self.window.mimics.all()[0], new_mimic)

    def test_add_mimic_page_redirects_after_POST(self):
        response = self.client.post(self.manage_mimic_url, data={'window': self.window.pk})
        self.assertRedirects(response, self.manage_mimic_url)

    def test_add_mimic_message(self):
        response = self.client.post(self.manage_mimic_url, data={'window': self.window.pk})
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level_tag, 'success')
        self.assertIn(messages_list[0].message, 'Mimic was added.')

    def test_add_mimic_print_message(self):
        response = self.client.post(self.manage_mimic_url, data={'window': self.window.pk})
        response_redirected = self.client.get(response.url)
        self.assertIn('Mimic was added.', response_redirected.rendered_content)