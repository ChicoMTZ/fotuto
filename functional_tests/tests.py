from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class UsersTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_visitors_cant_view_login_form_only(self):
        self.fail('Create this test!')

    def test_supervisor_can_view_mimics_and_charts(self):
        # A visitor go to Fotuto homepage
        self.browser.get(self.live_server_url)

        # Visitor notice page title and header mention "Fotuto"
        self.assertIn("Fotuto", self.browser.title)

        # A login form is shown
        # Since visitor have supervisor credentials he type it and proceed to log-in
        # TODO: Test login form

        # Then default mimic page is shown

        # Page title and header mention "Mimics"
        self.check_page_title_and_header(title="Mimics", header="Mimics")

        # A welcome message and the operator's name
        welcome_text = self.browser.find_element_by_id('welcome').text
        self.assertEqual("Welcome Elpidio", welcome_text)

        # Menus displays options to view items
        # TODO: If there are more than 1 mimic window no submenu is shown, else list of windows is shown, the same for
        #   History Charts

        # Link to mimic page is active
        menu_active = self.browser.find_element_by_css_selector('nav li.active')
        self.assertEqual("Mimics", menu_active.text)

        # A link to chart page
        menu_chart_link = self.browser.find_element_by_link_text('History charts')
        self.assertTrue(menu_chart_link.get_attribute('href').endswith('/history/'))

        # Following elements appears in the content:

        # A device name is shown
        device_name = self.browser.find_elements_by_css_selector('.mimic .title')[0].text
        self.assertEqual("Router", device_name)

        # A variable value indicator and variable's name
        var_item = self.browser.find_elements_by_css_selector('.mimic .var')[0]
        self.assertEqual("ON", var_item.text)
        self.assertEqual("Working", var_item.get_attribute('title'))

        # A message with last update timestamp
        last_updated_text = self.browser.find_element_by_id('last_updated_notificaion').text
        self.assertIn("Last updated: ", last_updated_text)
        # TODO: Check for the time

        # He notice last update timestamp changed every 3 seconds
        # Then he want to view the chart and click on the link
        # Page is updates with new elements:
        # Chart area is shown
        # An input box to enter a date
        # He notice data plotted in chart change on every update
        # He want to see yesterday chart and enter a date for yesterday in the input box and submit
        # Then Chart area is shown with new data
        self.fail('Finish the test!')

    def test_operator_can_add_vars_to_window(self):
        # A operator go to add var page
        self.browser.get('%s/vars/add/' % self.live_server_url)

        # A login form is shown
        # Operator type his credential and proceed to log-in
        # TODO: Test login form

        # TODO: Check operator menu
        # Operator have more options to customize the scada:
        # Menus:
        # * Mimics -> Add -> Window
        # * Mimics -> Add -> Device
        # * Mimics -> Add -> Var
        # * Mimics -> Add -> Mimic
        # * Mimics -> Manage -> Windows
        # * Mimics -> Manage -> Devices
        # * Mimics -> Manage -> Vars
        # * Mimics -> Manage -> Mimic
        # * History -> Add -> Chart
        # * History -> Manage -> Charts

        # Since there is not devices to attach a variable it is redirected to add a device
        # He notes Add Device page
        self.check_page_title_and_header(title="Add Device", header="Add Device")
        # He notice breadcrumbs (devices > add new)
        self.check_breadcrumbs((("Devices", '/devices/'), ("Add new",)))
        # He notes enter device first notification
        self.check_notification_message("Please, add a device first", 'info')

        # Enter device data
        device_name = 'Router'
        input_name = self.browser.find_element_by_id('id_name')
        # TODO: self.assertEqual(input_name.get_attribute('placeholder'), 'Name of the Device')
        input_name.send_keys(device_name)
        input_name = self.browser.find_element_by_id('id_address')
        input_name.send_keys('1234')

        # Submit form to add device
        btn_submit = self.browser.find_element_by_css_selector('.btn-primary')
        btn_submit.click()

        # He notice the added device confirmation message
        self.check_notification_message("Device was added")

        # Operator goes to add var page
        # TODO: Use menu to find link?
        self.browser.get('%s/vars/add/' % self.live_server_url)
        self.check_page_title_and_header(title="Add Variable", header="Add Variable")

        # He notice breadcrumbs (vars > add new)
        self.check_breadcrumbs((("Variables", '/vars/'), ("Add new",)))

        # Enter variable data
        var_name = 'Low Battery'
        input_var_name = self.browser.find_element_by_id('id_name')
        # TODO: self.assertEqual(input_name.get_attribute('placeholder'), 'Name of the variable')
        input_var_name.send_keys(var_name)
        # Select device
        select_var_device = self.browser.find_element_by_id('id_device')
        select_var_device.send_keys(Keys.ARROW_DOWN)
        # Specify a value
        input_var_value = self.browser.find_element_by_id('id_value')
        input_var_value.send_keys('1.0')

        # Submit form to add var
        btn_submit = self.browser.find_element_by_css_selector('.btn-primary')
        btn_submit.click()

        # It is redirected to var list
        # Confirmation message is shown
        self.check_notification_message("Variable was added")

        # In the list appears new var added
        table = self.browser.find_element_by_class_name('table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(var_name in row.text for row in rows)
        )

        # Add new added variable to window
        # Since a new device with a variable was added, automatically new mimic with var was created
        # So create new window
        self.browser.get('%s/windows/add/' % self.live_server_url)
        self.check_page_title_and_header(title="Add Window", header="Add Window")
        # He notice breadcrumbs (windows > add new)
        self.check_breadcrumbs((("Windows", '/windows/'), ("Add new",)))

        # Enter window data
        window_title = 'Main window'
        input_title = self.browser.find_element_by_id('id_title')
        # TODO: self.assertEqual(input_name.get_attribute('placeholder'), 'Title of the window')
        input_title.send_keys(window_title)

        # Submit form to add window
        btn_submit = self.browser.find_element_by_css_selector('.btn-primary')
        btn_submit.click()

        # Now he is in windows list page
        self.check_page_title_and_header(title="Windows", header="Windows")
        # He notice breadcrumbs
        self.check_breadcrumbs((("Windows",),))

        # So click in manage mimics button of a first
        # FIXME: This flow should be change in favor of a wizard
        button_manage_mimic = self.browser.find_elements_by_class_name('manage-mimics')[0]
        button_manage_mimic.click()

        # Now he is in manage mimics for the window page
        self.check_page_title_and_header(title="Manage Mimics", header="Manage Mimics")
        # He notice breadcrumbs (windows > Window.Title > Mimics)
        self.check_breadcrumbs((("Windows", '/windows/'), (window_title, '/windows/main-window/'), ("Mimics",),))

        # Add mimic to window
        mimic_name = "Router"
        input_mimic_name = self.browser.find_element_by_id('id_name')
        input_mimic_name.send_keys(mimic_name)
        # Specify var
        select_mimic_vars = self.browser.find_element_by_id('id_vars')
        select_mimic_vars.send_keys(Keys.ARROW_DOWN)
        # Left other mimic field with it default values
        # TODO: Enter position values and check them in window details page

        # Submit form to add mimic to window
        btn_submit = self.browser.find_element_by_css_selector('.btn-primary')
        btn_submit.click()

        # TODO: Add mimic from device (use name and vars from device)

        # Confirmation message is shown
        self.check_notification_message("Mimic was added")

        # Go to window details page (using breadcrumbs)
        button_view = self.browser.find_elements_by_link_text(window_title)[0]
        button_view.click()

        # Now he is details window page
        self.check_page_title_and_header(title=window_title, header=window_title)
        # He notice breadcrumbs (windows > Window.Title)
        self.check_breadcrumbs((("Windows", '/windows/'), (window_title,),))

        # Then mimic for device with new variable is shown
        mimic_name_html = self.browser.find_elements_by_css_selector('.mimic .name')[0].text
        self.assertEqual(mimic_name_html, mimic_name)

        # A variable value indicator and variable's name
        var_item = self.browser.find_elements_by_css_selector('.mimic .var')[0]
        self.assertEqual("1.0", var_item.text)
        self.assertEqual(var_name, var_item.get_attribute('title'))

    def check_page_title_and_header(self, url=None, title=None, header=None):
        """Checks if a page have specified title and header.
        :param url: Relative path to page, with start and end sash if None use current page (default None)
        :param title: Text in browser title (default: None)
        :param header: Text in main page heading (default: None)
        """
        if url is not None:
            self.browser.get('%s%s' % (self.live_server_url, url))
        if title is not None:
            self.assertIn(title, self.browser.title)

        header_text = self.browser.find_element_by_id('header_text').text
        if header is not None:
            self.assertIn(header, header_text)

    def check_notification_message(self, message, tag='success'):
        """
        Checks for a notification message in page.

        :param message: Text in message
        :param tag: Message tag level in lowercase (default: success)
        """
        var_added_confirmation = self.browser.find_element_by_class_name('alert')
        self.assertIn('alert-%s' % tag, var_added_confirmation.get_attribute('class'))
        self.assertIn(message, var_added_confirmation.text)

    def check_breadcrumbs(self, items):
        """
        Check for breadcrumbs in current page.

        :param items: list of tuple for items in breadcrumb, each tuple contain:
            0: Visible text displayed
            1: url: Last portion of url (empty for current active item)
        """
        breadcrumbs = self.browser.find_element_by_class_name('breadcrumb')
        # TODO: Check breadcrumb items order
        for item in items:
            if len(item) > 1:  # Has url
                breadcrumb_item = breadcrumbs.find_element_by_link_text(item[0])
                self.assertTrue(breadcrumb_item.get_attribute('href').endswith(item[1]))
            else:
                breadcrumb_item_text = breadcrumbs.find_element_by_css_selector('li.active').text
                self.assertEqual(breadcrumb_item_text, item[0])