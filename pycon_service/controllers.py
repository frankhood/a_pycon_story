import logging
from datetime import datetime

from django.utils.module_loading import import_string

from pycon_service import exceptions as api_exceptions, settings as app_settings
from pycon_service.clients import UserClient
from pycon_service.utils import is_adult_step_2

logger = logging.getLogger(__name__)


class UserController:
    def __init__(self, client: UserClient = None) -> None:
        """
        Grazie a locate possiamo recuperare la classe del client dai settings.
        Molto utile nei test di integrazione per evitare che vengano effettuate chiamate a sistemi esterni, quando non volute.
        E' sufficiente, nei setting di test, inserire USER_CLIENT_CLASS con un client mockato.

        Passare il client al controller invece permette di scegliere quale client agganciare (sarebbe possibile anche
        tramite override settings) ed essere molto parlanti sulla configurazione che si sta testando.
        """
        if client:
            self.client = client
        else:
            self.client = import_string(app_settings.USER_CLIENT_CLASS)()  # type: ignore

    def user_is_adult(self, remote_id: str) -> bool:
        """
        Interroga il client per ottenere la data di nascita dello user con quel remote_id e stabilire se
        è maggiorenne.
        @params: remote_id
        @output: bool
        """
        try:
            response_data = self.client.get_user_birth_date(remote_id)
            birth_date = datetime.strptime(response_data.birth_date, "%Y-%m-%d").date()
            return is_adult_step_2(birth_date)
        except api_exceptions.RequestDataErrorException as ex:
            logger.error("Request data error raised calling remote service")
            raise ex
        except api_exceptions.UnauthorizedRequestException as ex:
            logger.exception("Unauthorized request raised calling remote service")
            raise ex
        except api_exceptions.UnexpectedResponseException as ex:
            logger.exception("Unexpected response raised calling remote service")
            raise ex
        except Exception as ex:
            logger.exception("Unexpected exception raised calling remote service")
            raise ex
