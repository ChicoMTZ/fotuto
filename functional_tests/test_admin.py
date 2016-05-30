from django.contrib.auth.models import User

from .base import FunctionalTest


class AdminTest(FunctionalTest):
    def setUp(self):
        super(AdminTest, self).setUp()
        self.admin_data = {'username': 'admin', 'password': '123', 'email': 'admin@fotuto.org'}
        User.objects.create_superuser(**self.admin_data)

    def check_text_django_by_fotuto(self):
        self.assertIn("Fotuto", self.browser.title)
        site_name = self.browser.find_element_by_id('site-name').text
        self.assertIn("Fotuto", site_name)

        # It should not display Django text
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("Django", page_text)

    def test_display_fotuto_instead_of_django(self):

        # Login page should display fotuto
        self.browser.get('%s%s' % (self.server_url, '/admin/'))
        self.check_text_django_by_fotuto()

        # Login
        self.browser.find_element_by_name('username').send_keys(self.admin_data['username'])
        self.browser.find_element_by_name('password').send_keys(self.admin_data['password'])
        self.browser.find_element_by_css_selector('[type=submit]').click()

        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn("welcome", page_text.lower())
        self.check_text_django_by_fotuto()

        # Check for pages inside
        self.browser.find_element_by_link_text('Groups').click()
        self.check_text_django_by_fotuto()
