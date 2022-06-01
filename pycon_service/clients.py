import requests
from pydantic import BaseModel

from pycon_service import exceptions, settings as app_settings


class UserBirthDateResponseData(BaseModel):
    birth_date: str


class UserClient:
    def __init__(self) -> None:
        self.api_key = app_settings.USER_SERVICE_API_KEY
        self.base_url = app_settings.USER_SERVICE_BASE_URL

        if not (self.api_key and self.base_url):
            raise exceptions.ClientImproperlyConfiguredException("Client improperly configured")

    def _handle_error_response(self, response) -> None:
        if response.status_code == 400:
            raise exceptions.RequestDataErrorException(
                message="Request data errors",
                status_code=response.status_code,
                service_url=response.url,
                request_data=response.request,
                response_data=response.json(),
            )
        elif response.status_code in [401, 403]:
            raise exceptions.UnauthorizedRequestException(
                message="Unauthorized Request",
                status_code=response.status_code,
                service_url=response.url,
                request_data=response.request,
                response_data=response.json(),
            )
        else:
            raise exceptions.UnexpectedResponseException(
                message="Unexpected Response from Server",
                status_code=response.status_code,
                service_url=response.url,
                request_data=response.request,
                response_data=response.json(),
            )

    def get(self, url):
        response = requests.get(url, headers={"Authorization": f"Bearer {self.api_key}"})
        if 200 <= response.status_code <= 299:
            return response.json()
        return self._handle_error_response(response)  # type: ignore

    def get_user_birth_date(self, remote_user_id: str) -> UserBirthDateResponseData:
        url = "{base_url}/user/{user_id}/".format(base_url=self.base_url, user_id=remote_user_id)
        try:
            return UserBirthDateResponseData(**self.get(url))
        except Exception as ex:
            raise ex
