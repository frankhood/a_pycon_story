import factory
import factory.django
import factory.fuzzy
from django.core.files.base import ContentFile

from pycon_service import models
from pycon_service.clients import UserBirthDateResponseData


class RemoteUserFactory(factory.django.DjangoModelFactory):
    remote_id = factory.Faker("uuid4")

    class Meta:
        """RemoteUserFactory Meta."""

        model = models.RemoteUser


class ResourceFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")

    class Meta:
        model = models.Resource

    class Params:
        upload_file = factory.Trait(file=ContentFile(content="Test Content File", name="file_test.txt"))

    @factory.post_generation
    def remote_users(self, create, remote_users, **kwargs):
        if not create:
            return
        if remote_users:
            for remote_user in remote_users:
                self.remote_users.add(remote_user)


class UserBirthDateFactory(factory.Factory):
    class Meta:
        model = UserBirthDateResponseData

    @factory.lazy_attribute
    def birth_date(self):
        from faker import Factory

        fake = Factory.create()
        return fake.date_time_between(start_date="-30y", end_date="-1y").strftime("%Y-%m-%d")


class UserBirthDateAdultFactory(factory.Factory):
    class Meta:
        model = UserBirthDateResponseData

    @factory.lazy_attribute
    def birth_date(self):
        from faker import Factory

        fake = Factory.create()
        return fake.date_time_between(start_date="-30y", end_date="-19y").strftime("%Y-%m-%d")


class UserBirthDateNotAdultFactory(factory.Factory):
    class Meta:
        model = UserBirthDateResponseData

    @factory.lazy_attribute
    def birth_date(self):
        from faker import Factory

        fake = Factory.create()
        return fake.date_time_between(start_date="-18y", end_date="-1y").strftime("%Y-%m-%d")
