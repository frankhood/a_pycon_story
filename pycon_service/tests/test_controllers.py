import datetime
import uuid
from unittest.mock import patch

import pytz
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from pycon_service import exceptions as api_exceptions
from pycon_service.clients import UserBirthDateResponseData, UserClient
from pycon_service.controllers import UserController
from pycon_service.factories import RemoteUserFactory
from pycon_service.mocked_clients import (
    FakeBaseUserClient,
    MockedRequestDataErrorClient,
    MockedUnauthorizedRequestClient,
    MockedUnexpectedExceptionClient,
    MockedUnexpectedResponseClient,
)


# ==================================================================
# ./manage.py test pycon_service.tests.test_controllers.UserControllerIntegrationTest --configuration=Testing
# ==================================================================
class UserControllerIntegrationTest(TestCase):
    def test_user_is_adult_ok_passing_fake_client(self):
        # ==================================================================
        # ./manage.py test pycon_service.tests.test_controllers.UserControllerIntegrationTest.test_user_is_adult_ok_passing_fake_client --configuration=Testing
        # ==================================================================
        # Arrange
        remote_user = RemoteUserFactory()
        controller = UserController(client=FakeBaseUserClient({remote_user.remote_id: {"birth_date": "1999-3-22"}}))

        with freeze_time(
            timezone.make_aware(
                datetime.datetime(2017, 3, 21, 23, 59, 59),
                timezone=pytz.timezone("Europe/Rome"),
            )
        ):
            # Act
            is_adult = controller.user_is_adult(remote_user.remote_id)
            # Assert
            self.assertFalse(is_adult)
        with freeze_time(
            timezone.make_aware(
                datetime.datetime(2017, 3, 22, 0, 0, 0),
                timezone=pytz.timezone("Europe/Rome"),
            )
        ):
            # Act
            is_adult = controller.user_is_adult(remote_user.remote_id)
            # Assert
            self.assertTrue(is_adult)

    def test_mock_method(self):
        # ==================================================================
        # ./manage.py test pycon_service.tests.test_controllers.UserControllerIntegrationTest.test_mock_method --configuration=Testing
        # ==================================================================
        with patch.object(
            UserClient, "get_user_birth_date", return_value=UserBirthDateResponseData(birth_date="1999-3-22")
        ) as get_user_birth_date:
            response = UserClient.get_user_birth_date(remote_user_id=str(uuid.uuid4()))
            self.assertIsInstance(response, UserBirthDateResponseData)
            self.assertEqual(response.birth_date, "1999-3-22")
            get_user_birth_date.assert_called_once()

    def test_user_is_adult_ok_with_mock(self):
        # ==================================================================
        # ./manage.py test pycon_service.tests.test_controllers.UserControllerIntegrationTest.test_user_is_adult_ok_with_mock --configuration=Testing
        # ==================================================================
        # Arrange
        controller = UserController(client=UserClient())
        remote_user = RemoteUserFactory()

        with patch.object(
            UserClient, "get_user_birth_date", return_value=UserBirthDateResponseData(birth_date="1999-3-22")
        ):
            with freeze_time(
                timezone.make_aware(
                    datetime.datetime(2017, 3, 21, 23, 59, 59),
                    timezone=pytz.timezone("Europe/Rome"),
                )
            ):
                # Act
                is_adult = controller.user_is_adult(remote_user.remote_id)
                # Assert
                self.assertFalse(is_adult)
            with freeze_time(
                timezone.make_aware(
                    datetime.datetime(2017, 3, 22, 0, 0, 0),
                    timezone=pytz.timezone("Europe/Rome"),
                )
            ):
                # Act
                is_adult = controller.user_is_adult(remote_user.remote_id)
                # Assert
                self.assertTrue(is_adult)

    def test_user_is_adult_ko(self):
        # ==================================================================
        # ./manage.py test pycon_service.tests.test_controllers.UserControllerIntegrationTest.test_user_is_adult_ko --configuration=Testing
        # ==================================================================
        with self.subTest("Request data errors"):
            # Arrange
            controller = UserController(client=MockedRequestDataErrorClient())
            remote_user = RemoteUserFactory()
            # Act & Assert
            with self.assertRaises(api_exceptions.RequestDataErrorException):
                controller.user_is_adult(remote_user.remote_id)

        with self.subTest("Unauthorized request error"):
            # Arrange
            controller = UserController(client=MockedUnauthorizedRequestClient())
            remote_user = RemoteUserFactory()
            # Act & Assert
            with self.assertRaises(api_exceptions.UnauthorizedRequestException):
                controller.user_is_adult(remote_user.remote_id)

        with self.subTest("Unexpected response error"):
            # Arrange
            controller = UserController(client=MockedUnexpectedResponseClient())
            remote_user = RemoteUserFactory()
            # Act & Assert
            with self.assertRaises(api_exceptions.UnexpectedResponseException):
                controller.user_is_adult(remote_user.remote_id)

        with self.subTest("Unexpected exception error"):
            # Arrange
            controller = UserController(client=MockedUnexpectedExceptionClient())
            remote_user = RemoteUserFactory()
            # Act & Assert
            with self.assertRaises(Exception):
                controller.user_is_adult(remote_user.remote_id)

        with self.subTest("Format error"):
            # Arrange
            remote_user = RemoteUserFactory()
            controller = UserController(
                client=FakeBaseUserClient(configuration={remote_user.remote_id: {"birth_date": "5-12-2022"}})
            )
            # Act & Assert
            with self.assertRaisesMessage(ValueError, "time data '5-12-2022' does not match format '%Y-%m-%d'"):
                controller.user_is_adult(remote_user.remote_id)
