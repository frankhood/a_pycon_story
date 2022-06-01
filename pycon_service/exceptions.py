class BaseErrorResponseException(Exception):
    def __init__(
        self,
        message,
        status_code=None,
        service_url=None,
        request_data=None,
        response_data=None,
    ):
        self.message = message
        self.status_code = status_code
        self.service_url = service_url
        self.request_data = request_data
        self.response_data = response_data


class RequestDataErrorException(BaseErrorResponseException):
    def __str__(self):
        return (
            f"Wrong request data to url {self.service_url}: {self.message}\n"
            f"status_code : {self.status_code}\n"
            f"request_data : {self.request_data}\n"
            f"response_data : {self.response_data}"
        )


class UnauthorizedRequestException(BaseErrorResponseException):
    def __str__(self):
        return (
            f"Unauthorized request to url {self.service_url}: {self.message}\n"
            f"status_code : {self.status_code}\n"
            f"request_data : {self.request_data}\n"
            f"response_data : {self.response_data}"
        )


class UnexpectedResponseException(BaseErrorResponseException):
    def __str__(self):
        return (
            f"Unexpected response\n"
            f"status_code : {self.status_code}\n"
            f"request_data : {self.request_data}\n"
            f"response_data : {self.response_data}"
        )


class ClientImproperlyConfiguredException(BaseErrorResponseException):
    def __str__(self) -> str:
        return self.message
