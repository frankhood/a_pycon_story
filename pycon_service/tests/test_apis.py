from __future__ import absolute_import, print_function

import uuid
from typing import List

from django.core.files.base import ContentFile
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from pycon_service.factories import RemoteUserFactory, ResourceFactory
from pycon_service.models import RemoteUser, Resource


# =======================================================================
# ./manage.py test pycon_service.tests.test_apis.RemoteUserResourcesApiViewAPITest  --configuration=Testing
# =======================================================================
class RemoteUserResourcesApiViewAPITest(APITestCase):
    def setUp(self):
        super().setUp()
        self.api_client = APIClient()
        self.request_factory = APIRequestFactory()

    def get_resources_configuration(self, number_of_resources: int = 0, add_file: bool = False) -> List[Resource]:
        remote_user = RemoteUser.objects.create(
            remote_id=uuid.uuid4(),
        )
        resouces = []
        for x in range(number_of_resources):
            if add_file:
                resource = Resource.objects.create(
                    name=f"Resource {x}", file=ContentFile("Test Content File", "file_test.txt")
                )
            else:
                resource = Resource.objects.create(name=f"Resource {x}")
            resource.remote_users.set([remote_user])
            resouces.append(resource)
        return resouces

    def get_resources_configuration_with_multiple_users(
        self, number_of_resources_for_user: int = 0, number_of_users: int = 0, add_file: bool = False
    ) -> List[Resource]:
        resources = []
        for x in range(number_of_users):
            remote_user = RemoteUser.objects.create(
                remote_id=uuid.uuid4(),
            )
            for x in range(number_of_resources_for_user):
                if add_file:
                    resource = Resource.objects.create(
                        name=f"Resource {x}", file=ContentFile("Test Content File", "file_test.txt")
                    )
                else:
                    resource = Resource.objects.create(name=f"Resource {x}")
                resource.remote_users.set([remote_user])
                resources.append(resource)
        return resources

    def test_retrieve_remote_user_resources_200(self):
        # =======================================================================
        # ./manage.py test pycon_service.tests.test_apis.RemoteUserResourcesApiViewAPITest.test_retrieve_remote_user_resources_200  --configuration=Testing
        # =======================================================================
        # Arrange
        remote_user = RemoteUserFactory()
        for x in range(3):
            ResourceFactory(remote_users=[remote_user])

        # Act: FakeClient with import_string
        response = self.api_client.get(f"/api/v1/resources/{remote_user.remote_id}/")

        # Act: FakeClient passed to the API View
        # request = self.request_factory.get(f"/api/v1/resources/{remote_user.remote_id}/")
        # response = RemoteUserResourcesApiView.as_view(
        #     {"get": "list"},
        #     user_controller=UserController(
        #         client=FakeBaseUserClient(configuration={remote_user.remote_id: {"birth_date": "1999-3-22"}})
        #     ),
        # )(request, remote_id=remote_user.remote_id)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(sorted(response.data[0].keys()), sorted(["id", "name", "file", "created", "modified"]))

    def test_retrieve_remote_user_resources_403(self):
        # =======================================================================
        # ./manage.py test pycon_service.tests.test_apis.RemoteUserResourcesApiViewAPITest.test_retrieve_remote_user_resources_403  --configuration=Testing
        # =======================================================================
        remote_user = RemoteUserFactory()
        with self.subTest("User is not adult"):
            with override_settings(USER_CLIENT_CLASS="pycon_service.mocked_clients.FakeBaseNotAdultUserClient"):
                response = self.api_client.get(f"/api/v1/resources/{remote_user.remote_id}/")
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        with self.subTest("UserClient raise request data exception"):
            with override_settings(USER_CLIENT_CLASS="pycon_service.mocked_clients.MockedRequestDataErrorClient"):
                response = self.api_client.get(f"/api/v1/resources/{remote_user.remote_id}/")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        with self.subTest("UserClient raise unauthorized request exception"):
            with override_settings(USER_CLIENT_CLASS="pycon_service.mocked_clients.MockedUnauthorizedRequestClient"):
                response = self.api_client.get(f"/api/v1/resources/{remote_user.remote_id}/")
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        with self.subTest("UserClient raise unexpected response exception"):
            with override_settings(USER_CLIENT_CLASS="pycon_service.mocked_clients.MockedUnexpectedResponseClient"):
                response = self.api_client.get(f"/api/v1/resources/{remote_user.remote_id}/")
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        with self.subTest("UserClient raise unexpected exception"):
            with override_settings(USER_CLIENT_CLASS="pycon_service.mocked_clients.MockedUnexpectedExceptionClient"):
                response = self.api_client.get(f"/api/v1/resources/{remote_user.remote_id}/")
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_remote_user_resources_serializer_fields(self):
        # =======================================================================
        # ./manage.py test pycon_service.tests.test_apis.RemoteUserResourcesApiViewAPITest.test_retrieve_remote_user_resources_serializer_fields  --configuration=Testing
        # =======================================================================
        # Arrange
        remote_user = RemoteUserFactory()
        for x in range(3):
            ResourceFactory(remote_users=[remote_user], upload_file=True)
        # Act
        response = self.api_client.get(f"/api/v1/resources/{remote_user.remote_id}/")
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(
            sorted(response.json()[0].keys()),
            sorted(["id", "name", "file", "created", "modified"]),
        )
