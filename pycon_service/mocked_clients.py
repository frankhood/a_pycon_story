from typing import Any, Dict, NoReturn

from django.core.exceptions import ImproperlyConfigured

from pycon_service import exceptions as api_exceptions
from pycon_service.factories import UserBirthDateAdultFactory, UserBirthDateFactory, UserBirthDateNotAdultFactory


class FakeBaseUserClient:
    def __init__(self, configuration: Dict[str, Any] = None) -> None:
        self.configuration = configuration or {}

    def get(self, url: str):
        raise ImproperlyConfigured("You shouldn't be here!")

    def get_user_birth_date(self, remote_user_id: str) -> Dict[str, str]:
        configuration_for_user = self.configuration.get(remote_user_id, None)
        if configuration_for_user:
            return UserBirthDateFactory(birth_date=configuration_for_user.get("birth_date", ""))
        return UserBirthDateFactory()


class FakeBaseNotAdultUserClient:
    def get_user_birth_date(self, remote_user_id: str) -> Dict[str, str]:
        return UserBirthDateNotAdultFactory()


class FakeBaseAdultUserClient:
    def get_user_birth_date(self, remote_user_id: str) -> Dict[str, str]:
        return UserBirthDateAdultFactory()


class MockedRequestDataErrorClient:
    def get_user_birth_date(self, remote_user_id: str) -> NoReturn:
        raise api_exceptions.RequestDataErrorException("Exception")


class MockedUnauthorizedRequestClient:
    def get_user_birth_date(self, remote_user_id: str) -> NoReturn:
        raise api_exceptions.UnauthorizedRequestException("Exception")


class MockedUnexpectedResponseClient:
    def get_user_birth_date(self, remote_user_id: str) -> NoReturn:
        raise api_exceptions.UnexpectedResponseException("Exception")


class MockedUnexpectedExceptionClient:
    def get_user_birth_date(self, remote_user_id: str) -> NoReturn:
        raise Exception("Exception")
