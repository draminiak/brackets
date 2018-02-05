from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import RequestFactory
from unittest.mock import patch, MagicMock
from ddt import ddt, data, unpack

from webapp.lib.registration import Registration
from webapp.forms import UserRegistrationForm


@ddt
class TestRegistration(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestRegistration, cls).setUpClass()
        User.objects.create(username='testExists', password='passwd', email='test@testExists.com')

    @data(
        (RequestFactory().get('/register/')),
        (RequestFactory().post('/register/')),
        (RequestFactory().post('/register', {})),
        (RequestFactory().post('/register', {'FOO': 'bar'})),
    )
    def test_init(self, request):
        reg = Registration(request)
        self.assertIsNotNone(reg.request, msg='Request object should be populated on init as it was passed into the constructor')
        self.assertIsNotNone(reg.form, 'Registration form should be populated on init')
        self.assertIsInstance(reg.form, UserRegistrationForm, msg='Form object is the wrong class'), 

    @patch('webapp.lib.registration.Registration._Registration__create_user')
    @data(
        # Invalid POST data
        [RequestFactory().get('/register/'), 0],
        [RequestFactory().post('/register/'), 0],
        [RequestFactory().post('/register', {}), 0],
        [RequestFactory().post('/register', {'FOO': 'bar'}), 0],
        # Duplicate username, email
        [RequestFactory().post('/register', {'username': 'testExists', 'password': 'passwd', 'email': 'test@test.com'}), 0],
        [RequestFactory().post('/register', {'username': 'test', 'password': 'passwd', 'email': 'test@testExists.com'}), 0],
        # Valid POST data
        [RequestFactory().post('/register', {'username': 'test', 'password': 'passwd', 'email': 'test@test.com'}), 1],
    )
    @unpack
    def test_process__valid_post_data_calls_create(self, request, num_create, mock_create):
        reg = Registration(request)
        reg.process()
        self.assertEqual(mock_create.called, num_create, 
                            msg='__create_user() was not called {} times (actual={})'.format(num_create, mock_create.called))

    @patch('webapp.lib.registration.login')
    @data(
        [RequestFactory().post('/register', {'username': 'test', 'password': 'passwd', 'email': 'test@test.com'}), True],
        [RequestFactory().post('/register', {'username': 'testExists', 'password': 'passwd', 'email': 'test@test.com'}), False],
        [RequestFactory().post('/register', {'username': 'test', 'password': 'passwd', 'email': 'test@testExists.com'}), False],
        [RequestFactory().post('/register', {'username': 'testExists', 'password': 'passwd', 'email': 'test@testExists.com'}), False],
    )
    @unpack
    def test_process__create_user(self, request, expect_unique, mock_login):
        reg = Registration(request)
        reg.process()
        self.assertEqual(mock_login.called, int(expect_unique), 
                            msg='login() was not called {} times (actual={})'.format(1, mock_login.called))
