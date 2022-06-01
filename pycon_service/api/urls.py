from django.urls import path

from pycon_service.api import views as api_views

app_name = "pycon_service_api"


urlpatterns = [
    path(
        "resources/<uuid:remote_id>/",
        api_views.RemoteUserResourcesApiView.as_view({"get": "list"}),
        name="user-resources-api",
    ),
]
