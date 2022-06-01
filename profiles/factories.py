# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

import factory
import pytz
from django.utils.translation import ugettext, ugettext_lazy as _  # noqa

from . import models

logger = logging.getLogger(__name__)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        """User factory Meta."""

        model = models.User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttribute(lambda a: "{0}.{1}@mailinator.com".format(a.first_name, a.last_name).lower())
    email = factory.LazyAttribute(lambda a: a.username)
    date_joined = factory.Faker(
        "date_time_this_year",
        before_now=True,
        after_now=False,
        tzinfo=pytz.timezone("Europe/Rome"),
    )
    # date_joined = factory.LazyFunction(datetime.datetime.now)

    @factory.post_generation
    def password(self, create, raw_password=None, **kwargs):
        if not create:
            return
        if raw_password:
            self.set_password(raw_password)
        else:
            self.set_unusable_password()


class StaffUserFactory(UserFactory):
    class Meta:
        """Staff User factory Meta."""

        model = models.User

    first_name = "Staff"
    last_name = "User"
    is_staff = True


class SuperUserFactory(UserFactory):
    class Meta:
        """SuperUser factory Meta."""

        model = models.User

    first_name = "Super"
    last_name = "User"
    is_staff = True
    is_superuser = True
