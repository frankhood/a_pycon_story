import logging

from rest_framework.permissions import BasePermission

from pycon_service import exceptions as api_exceptions

logger = logging.getLogger(__name__)


class UserIsAdultPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            return view.get_user_controller().user_is_adult(view.kwargs.get("remote_id"))
        except (
            api_exceptions.RequestDataErrorException,
            api_exceptions.UnauthorizedRequestException,
            api_exceptions.UnexpectedResponseException,
        ):
            return False
        except Exception as ex:
            logger.exception("Unexpected exception during check permissions", extra={"exception": str(ex.__dict__)})
            return False
