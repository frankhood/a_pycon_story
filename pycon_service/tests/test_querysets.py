from django.test.testcases import TestCase

from pycon_service.factories import RemoteUserFactory, ResourceFactory
from pycon_service.models import Resource


# =======================================================================
# ./manage.py test pycon_service.tests.test_querysets.ResourceQuerySetTest  --configuration=Testing
# =======================================================================
class ResourceQuerySetTest(TestCase):
    def test_for_user(self):
        # =======================================================================
        # ./manage.py test pycon_service.tests.test_querysets.ResourceQuerySetTest.test_for_user  --configuration=Testing
        # =======================================================================
        # Arrange
        remote_user = RemoteUserFactory()
        resource_one = ResourceFactory(remote_users=[remote_user])
        resource_two = ResourceFactory()
        # Act
        resources = Resource.objects.for_user(remote_user.remote_id)
        # Assert
        self.assertIn(resource_one, resources)
        self.assertNotIn(resource_two, resources)
