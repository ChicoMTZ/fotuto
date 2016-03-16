from django.contrib.auth import get_user_model
from django.core.urlresolvers import resolve
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from mimics.models import Mimic
from vars.models import Device, Var
from windows.models import Window

# TODO: In production API should only available over https
# TODO: Api must require permissions for some actions like POST, PUT, DELETE?
# TODO: Inactive items should not be returned by default, only will be visible if specific paramter is passed (i.e.
#     ``inactive=true``)
# TODO: Refactor Api Tests classes

User = get_user_model()


class APIAuthentication(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@mail.com', '123')
        self.token = Token.objects.get_or_create(user=self.user)[0].key

    def test_unauthorized_access(self):
        """Users should be authenticated to access to the api"""
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 403, response.data)
        unauthenticated_error = {
            u'detail': u'Authentication credentials were not provided.'
        }
        self.assertDictEqual(response.data, unauthenticated_error)

    def test_obtain_token(self):
        """Registered users can request for a token"""
        user2 = User.objects.create_user('user2', 'user2@mail.com', '123')
        response = self.client.post('/api-token-auth/', {'username': user2.username, 'password': '123'})
        self.assertEqual(response.status_code, 200, response.data)
        self.assertTrue('token' in response.data)
        # TODO: Test for not empty or null token value

    def test_authorization(self):
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
        response = self.client.get('/api/', {}, **header)
        self.assertEqual(response.status_code, 200, "REST token-auth failed")

    def test_root_endpoints(self):
        """Tests for default root endpoints"""
        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
        response = self.client.get('/api/', {}, **header)
        # TODO: This also should display devices
        default_endpoints = {
            "windows": "http://testserver/api/windows/",
            "devices": "http://testserver/api/devices/",
            "users": "http://testserver/api/users/",
        }
        self.assertDictEqual(response.data, default_endpoints)


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.operator = User.objects.create_user(
            username="maceo", first_name="Jose", last_name="Maceo", password='123'
        )
        self.supervisor = User.objects.create_user(
            username="marti", first_name="Jose", last_name="Marti", password='123'
        )
        self.token = Token.objects.get_or_create(user=self.operator)[0].key
        self.auth_header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}

    def test_user_route(self):
        """Test that we've got routing set up for a User"""
        route = resolve('/api/users/marti/')
        self.assertEqual(route.func.__name__, 'UserViewSet')

    def test_user_get_return_correct_data(self):
        """Test that we can get a User"""
        response = self.client.get('/api/users/marti/', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        operator_data = {
            'id': self.supervisor.pk,
            'username': self.supervisor.username,
            'full_name': "Jose Marti",
            'is_active': self.supervisor.is_active,
            'links': {
                'self': 'http://testserver/api/users/marti/'
            }
        }
        self.assertDictEqual(response.data, operator_data)

    def test_users_list_route(self):
        """Test that we've got routing set up for Users"""
        route = resolve('/api/users/')
        self.assertEqual(route.func.__name__, 'UserViewSet')

    def test_users_list(self):
        """Test that we can get a list of users"""
        response = self.client.get('/api/users/', {}, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'], "maceo")
        self.assertEqual(response.data[1]['username'], "marti")

    def test_user_create(self):
        """Test that we can create a User"""
        user_data = {
            'username': "ernesto",
            'password': "123",
        }
        response = self.client.post('/api/users/', data=user_data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)


class WindowAPITestCase(APITestCase):
    def setUp(self):
        self.window_1_data = {
            'title': "Some Windows",
            'slug': "some-windows",
            'description': "The first window",
        }
        self.window_1 = Window.objects.create(**self.window_1_data)
        self.window_2 = Window.objects.create(
            title="Some Windows 2",
            slug="some-windows-2",
            description="The second window"
        )
        self.user = User.objects.create_user('user', 'user@mail.com', '123')
        self.token = Token.objects.get_or_create(user=self.user)[0].key
        self.auth_header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}

    def test_list_windows(self):
        """Test that we can get a list of windows"""
        response = self.client.get('/api/windows/', {}, **self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], "Some Windows")
        self.assertEqual(response.data[1]['description'], 'The second window')

    def test_windows_list_route(self):
        """Test that we've got routing set up for Windows"""
        route = resolve('/api/windows/')
        self.assertEqual(route.func.__name__, 'WindowViewSet')

    def test_unauthenticated_cant_create_window(self):
        """Test that unauthenticated user can't create a Window"""
        post_data = {
            'title': "Window 3",
            'slug': 'window-3',
            'description': "The third window",
        }
        response = self.client.post('/api/windows/', data=post_data, format='json')
        self.assertEqual(response.status_code, 403, response.data)
        unauthenticated_error = {
            u'detail': u'Authentication credentials were not provided.'
        }
        self.assertDictEqual(response.data, unauthenticated_error)

    def test_create_window(self):
        """Test that we can create a Window"""
        post_data = {
            'title': "Window 3",
            'slug': 'window-3',
            'description': "The third window",
        }
        response = self.client.post('/api/windows/', data=post_data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, 201, response.data)
        self.assertDictContainsSubset(post_data, response.data)

    def test_window_get_return_correct_data(self):
        """Test that we can get a Window"""
        window_1_url_path = '/api/windows/%s/' % self.window_1.pk
        response = self.client.get(window_1_url_path, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        windows_data = self.window_1_data.copy()
        windows_data.update({
            'id': self.window_1.pk,
            'links': {
                'self': 'http://testserver%s' % window_1_url_path
            }
        })
        self.assertDictEqual(response.data, windows_data)


class DeviceAPITestCase(APITestCase):
    def setUp(self):
        self.device_1_data = {
            'name': "Some Device 1",
            'slug': "some-device-1",
            'active': True,
            'model': "AA1",
            'address': "0001",
            'description': "Some description"
        }
        self.device_1 = Device.objects.create(**self.device_1_data)
        self.device_2 = Device.objects.create(
            name="Some Device 2",
            slug="some-device-2",
            active=True,
            model="AA2",
            address="0002",
            description="Some description 2"
        )
        self.user = User.objects.create_user('user', 'user@mail.com', '123')
        self.token = Token.objects.get_or_create(user=self.user)[0].key
        self.auth_header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}

    def test_list_device(self):
        """Test that we can get a list of Devices"""
        response = self.client.get('/api/devices/', **self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], "Some Device 1")
        self.assertEqual(response.data[1]['address'], "0002")

    def test_devices_list_route(self):
        """Test that we've got routing set up for Device"""
        route = resolve('/api/devices/')
        self.assertEqual(route.func.__name__, 'DeviceViewSet')

    def test_create_device(self):
        """Test that we can create a Device"""
        device_data = {
            'name': "Some Device",
            'slug': "some-device",
            'active': True,
            'model': "AA3",
            'address': "0003",
            'description': "Some description",
        }
        response = self.client.post('/api/devices/', data=device_data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, 201, response.data)
        created_device = Device.objects.get(**device_data)
        device_data.update({'id': created_device.pk})
        self.assertDictContainsSubset(device_data, response.data)

    def test_device_get_return_correct_data(self):
        """Test that we can get a Device"""
        device_1_url_path = '/api/devices/%s/' % self.device_1.pk
        response = self.client.get(device_1_url_path, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        device_data = self.device_1_data.copy()
        device_data.update({
            'id': self.device_1.pk,
            'links': {
                'self': 'http://testserver%s' % device_1_url_path
            }
        })
        self.assertDictEqual(response.data, device_data)


class VarAPITestCase(APITestCase):
    def setUp(self):
        self.device_1 = Device.objects.create(
            name="Door 1 Sensor",
            slug="door-1-sensor",
            active=True,
            model="ISUDS-1",
            address="0002",
            description="Sensor for front door"
        )
        self.var_door_1_state_data = {
            'name': "Door 1 State",
            'slug': "door-1-sate",
            'active': True,
            'device': self.device_1,
            'var_type': "binary",
            'value': 1,
            'description': "Door 1 state: 1=Open, 0=Closed"
        }
        self.var_door_1_state = Var.objects.create(**self.var_door_1_state_data)
        self.var_2 = Var.objects.create(
            name="Door 1 Communication",
            slug="door-1-comm",
            active=True,
            device=self.device_1,
            var_type="binary",
            value=1,
            description="Communication state with door 1 sensor: 1=Yes, 0=No"
        )
        self.user = User.objects.create_user('user', 'user@mail.com', '123')
        self.token = Token.objects.get_or_create(user=self.user)[0].key
        self.auth_header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}

    def test_list_vars(self):
        """Test that we can get a list of Variables"""
        response = self.client.get('/api/vars/', **self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], "Door 1 State")
        self.assertEqual(response.data[1]['slug'], "door-1-comm")

    def test_vars_list_route(self):
        """Test that we've got routing set up for Variables"""
        route = resolve('/api/vars/')
        self.assertEqual(route.func.__name__, 'VarViewSet')

    def test_create_variable(self):
        """Test that we can create a Variable"""
        controller_device = Device.objects.create(
            name="Controller-1",
            slug="controller-1",
            active=True,
            model="ISUCALARM-1",
            address="0001",
            description="Controller for the alarm system"
        )
        var_data = {
            'name': "Alarm State",
            'slug': "alarm-state",
            'active': True,
            'device': controller_device.pk,
            'var_type': "binary",
            'units': "",
            'value': 0,
            'description': "Alarm state: 1=Activated, 0=Deactivated"
        }
        response = self.client.post('/api/vars/', data=var_data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, 201, response.data)
        created_var = Var.objects.get(**var_data)
        var_data.update({'id': created_var.pk})
        self.assertDictContainsSubset(var_data, response.data)

    def test_get_var_return_correct_data(self):
        """Test if returned var includes the `var_type` also in a human readable format"""
        response = self.client.get('/api/vars/%s/' % self.var_door_1_state.pk, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.var_door_1_state_data.update({
            'id': self.var_door_1_state.pk,
            'var_type_display': self.var_door_1_state.get_var_type_display(),
            'device': self.var_door_1_state.device.pk,
            'value': 1.0,
            'units': '',
        })
        self.assertDictEqual(response.data, self.var_door_1_state_data)


class MimicAPITestCase(APITestCase):
    def setUp(self):
        self.device_alarm_controller = Device.objects.create(
            name="Alarm Controller",
            slug="alarm-controller",
            active=True,
            model="ISUCALARM-1",
            address="0001",
            description="Alarm Controller with arduino"
        )
        self.var_door_state = Var.objects.create(
            name="Door 1 State",
            slug="door-1-sate",
            active=True,
            device=self.device_alarm_controller,
            var_type="binary",
            value=1,
            description="Door 1 state: 1=Open, 0=Closed"
        )
        self.var_sensor_door_comm = Var.objects.create(
            name="Door 1 Communication",
            slug="door-1-comm",
            active=True,
            device=self.device_alarm_controller,
            var_type="binary",
            value=1,
            description="Communication state with door 1 sensor: 1=Yes, 0=No"
        )
        self.var_alarm_state = Var.objects.create(
            name="Alarm State",
            slug="alarm-state",
            active=True,
            device=self.device_alarm_controller,
            var_type="binary",
            value=0,
            description="Alarm state: 1=Activated, 0=Deactivated"
        )
        self.window_security = Window.objects.create(
            title="Security",
            slug="security",
            description="Home Security System"
        )
        self.mimic_alarm_spotlight = Mimic.objects.create(
            name="Alarm Spotlight",
            window=self.window_security,
            x=0,
            y=0
        )
        self.mimic_alarm_spotlight.vars.add(self.var_alarm_state)
        self.mimic_sensor_front_door = Mimic.objects.create(
            name="Front Door Sensor",
            window=self.window_security,
            x=100,
            y=0
        )
        self.mimic_sensor_front_door.vars.add(self.var_door_state)
        self.mimic_sensor_front_door.vars.add(self.var_sensor_door_comm)

        self.user = User.objects.create_user('user', 'user@mail.com', '123')
        self.token = Token.objects.get_or_create(user=self.user)[0].key
        self.auth_header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}

    def test_list_mimics(self):
        """Test that we can get a list of Mimics"""
        response = self.client.get('/api/mimics/', **self.auth_header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], "Alarm Spotlight")
        self.assertEqual(response.data[1]['x'], 100)

    def test_mimics_list_route(self):
        """Test that we've got routing set up for Mimic"""
        route = resolve('/api/mimics/')
        self.assertEqual(route.func.__name__, 'MimicViewSet')

    def test_create_mimic(self):
        """Test that we can create a Mimic"""
        mimic_data = {
            'name': "Alarm Controller",
            'window': self.window_security.pk,
            'x': 0,
            'y': 1
        }
        response = self.client.post('/api/mimics/', data=mimic_data, format='json', **self.auth_header)
        self.assertEqual(response.status_code, 201, response.data)
        created_mimic = Mimic.objects.get(**mimic_data)
        mimic_data.update({'id': created_mimic.pk, 'vars': []})
        self.assertDictEqual(response.data, mimic_data)

        # TODO: By default mimic request should return vars info
        # TODO: Test list/view/create/update/delete vars to a mimic
