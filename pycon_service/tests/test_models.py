import datetime

from django.test.testcases import TestCase
from django.utils import timezone

from pycon_service.factories import RemoteUserFactory, ResourceFactory


def yesterday():
    return timezone.now() - datetime.timedelta(days=1)


# =======================================================================
# ./manage.py test pycon_service.tests.test_models.RemoteUserUnitTest  --configuration=Testing
# =======================================================================
class RemoteUserUnitTest(TestCase):
    def test_str(self):
        # =======================================================================
        # ./manage.py test pycon_service.tests.test_models.RemoteUserUnitTest.test_str  --configuration=Testing
        #  =======================================================================
        obj = RemoteUserFactory()
        self.assertEqual(obj.__str__(), f"{obj.remote_id}")


# =======================================================================
# ./manage.py test pycon_service.tests.test_models.ResourceUnitTest  --configuration=Testing
# =======================================================================
class ResourceUnitTest(TestCase):
    def test_str(self):
        # =======================================================================
        # ./manage.py test pycon_service.tests.test_models.ResourceUnitTest.test_str  --configuration=Testing
        #  =======================================================================
        obj = ResourceFactory(name="Test resource")
        self.assertEqual(obj.__str__(), f"{obj.name}")

    def test_uploaded_file(self):
        # =======================================================================
        # ./manage.py test pycon_service.tests.test_models.ResourceUnitTest.test_uploaded_file  --configuration=Testing
        #  =======================================================================
        res_one = ResourceFactory()
        res_two = ResourceFactory(upload_file=True)
        self.assertFalse(res_one.file)
        self.assertTrue(res_two.file)
        self.assertIn("file_test", res_two.file.name)
