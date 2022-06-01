from rest_framework import mixins, viewsets

from pycon_service.api.serializers import ResourceSerializer
from pycon_service.controllers import UserController
from pycon_service.models import Resource
from pycon_service.permissions import UserIsAdultPermission


class RemoteUserResourcesApiView(mixins.ListModelMixin, viewsets.GenericViewSet):

    permission_classes = (UserIsAdultPermission,)
    serializer_class = ResourceSerializer
    lookup_url_kwarg = "remote_id"
    lookup_field = "remote_user"
    user_controller = None

    def get_queryset(self):
        return Resource.objects.for_user(remote_id=self.kwargs.get("remote_id"))

    def get_user_controller(self):
        return self.user_controller or UserController()
