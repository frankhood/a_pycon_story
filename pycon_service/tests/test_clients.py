import uuid
from unittest.mock import patch

import requests
from django.conf import settings
from django.test import TestCase, override_settings

from pycon_service import exceptions as api_exceptions
from pycon_service.clients import UserBirthDateResponseData, UserClient
from pycon_service.factories import RemoteUserFactory


# ===========================================================
# ./manage.py test pycon_service.tests.test_clients.UserClientUnitTest --configuration=Testing
# ===========================================================
class UserClientUnitTest(TestCase):
    @override_settings(USER_SERVICE_API_KEY="test-api-key", USER_SERVICE_BASE_URL="http://test.com/")
    def test__handle_error_response(self):
        # ===========================================================
        # ./manage.py test pycon_service.tests.test_clients.UserClientUnitTest.test__handle_error_response --configuration=Testing
        # ===========================================================
        response = requests.Response()
        response._content = b'{"test": "test"}'
        response.request = {}
        with self.subTest("response 400"):
            response.status_code = 400
            with self.assertRaises(api_exceptions.RequestDataErrorException):
                UserClient()._handle_error_response(response)
        with self.subTest("response 401"):
            response.status_code = 401
            with self.assertRaises(api_exceptions.UnauthorizedRequestException):
                UserClient()._handle_error_response(response)
        with self.subTest("response 403"):
            response.status_code = 403
            with self.assertRaises(api_exceptions.UnauthorizedRequestException):
                UserClient()._handle_error_response(response)
        with self.subTest("response 500"):
            response.status_code = 500
            with self.assertRaises(api_exceptions.UnexpectedResponseException):
                UserClient()._handle_error_response(response)

    @override_settings(USER_SERVICE_API_KEY="test-api-key", USER_SERVICE_BASE_URL="http://test.com/")
    def test_get(self):
        # ===========================================================
        # ./manage.py test pycon_service.tests.test_clients.UserClientUnitTest.test_get --configuration=Testing
        # ===========================================================
        response = requests.Response()
        response._content = b'{"test": "test"}'
        response.request = {}
        with self.subTest("response 200"):
            response.status_code = 200
            with patch.object(requests, "get", return_value=response):
                response_data = UserClient().get(url="http://test.com/")
                self.assertEqual(response_data, {"test": "test"})
        with self.subTest("response 400"):
            response.status_code = 400
            with patch.object(requests, "get", return_value=response):
                with self.assertRaises(api_exceptions.RequestDataErrorException):
                    UserClient().get(url="http://test.com/")
        with self.subTest("response 401"):
            response.status_code = 401
            with patch.object(requests, "get", return_value=response):
                with self.assertRaises(api_exceptions.UnauthorizedRequestException):
                    UserClient().get(url="http://test.com/")
        with self.subTest("response 403"):
            response.status_code = 403
            with patch.object(requests, "get", return_value=response):
                with self.assertRaises(api_exceptions.UnauthorizedRequestException):
                    UserClient().get(url="http://test.com/")
        with self.subTest("response 500"):
            response.status_code = 500
            with patch.object(requests, "get", return_value=response):
                with self.assertRaises(api_exceptions.UnexpectedResponseException):
                    UserClient().get(url="http://test.com/")

    def test_get_user_birth_date_ok(self):
        # ===========================================================
        # ./manage.py test pycon_service.tests.test_clients.UserClientUnitTest.test_get_user_birth_date_ok --configuration=Testing
        # ===========================================================
        with patch.object(UserClient, "get", return_value={"birth_date": "2020-5-4"}) as get_mock_method:
            remote_user = RemoteUserFactory()
            response_data = UserClient().get_user_birth_date(remote_user_id=remote_user.remote_id)
            get_mock_method.assert_called_once_with(f"{settings.USER_SERVICE_BASE_URL}/user/{remote_user.remote_id}/")
            self.assertIsInstance(response_data, UserBirthDateResponseData)

    def test_get_user_birth_date_ko(self):
        # ===========================================================
        # ./manage.py test pycon_service.tests.test_clients.UserClientUnitTest.test_get_user_birth_date_ko --configuration=Testing
        # ===========================================================
        with self.subTest("response 400"):
            with patch.object(UserClient, "get", side_effect=api_exceptions.RequestDataErrorException("Exception")):
                with self.assertRaises(api_exceptions.RequestDataErrorException):
                    with patch.object(
                        requests, "get", side_effect=api_exceptions.RequestDataErrorException("Exception")
                    ):
                        UserClient().get_user_birth_date(remote_user_id=str(uuid.uuid4()))

        with self.subTest("response 401"):
            with patch.object(UserClient, "get", side_effect=api_exceptions.UnauthorizedRequestException("Exception")):
                with self.assertRaises(api_exceptions.UnauthorizedRequestException):
                    with patch.object(
                        requests, "get", side_effect=api_exceptions.UnauthorizedRequestException("Exception")
                    ):
                        UserClient().get_user_birth_date(remote_user_id=str(uuid.uuid4()))

        with self.subTest("response 500"):
            with patch.object(UserClient, "get", side_effect=api_exceptions.UnexpectedResponseException("Exception")):
                with self.assertRaises(api_exceptions.UnexpectedResponseException):
                    with patch.object(
                        requests, "get", side_effect=api_exceptions.UnexpectedResponseException("Exception")
                    ):
                        UserClient().get_user_birth_date(remote_user_id=str(uuid.uuid4()))

        with self.subTest("ClientImproperlyConfigured"):
            with override_settings(USER_SERVICE_API_KEY="", USER_SERVICE_BASE_URL=""):
                with self.assertRaises(api_exceptions.ClientImproperlyConfiguredException):
                    UserClient().get_user_birth_date(remote_user_id=str(uuid.uuid4()))
