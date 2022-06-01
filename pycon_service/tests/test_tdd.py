from datetime import date, datetime
from unittest import expectedFailure

import pytz
from django.conf import settings
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from pycon_service.utils import is_adult_step_1, is_adult_step_2

# def freezegun_utc_workaround(datetime):
#     return pytz.timezone(settings.TIME_ZONE).localize(datetime)


# ==================================================================
# ./manage.py test pycon_service.tests.test_tdd.TDDTest --configuration=Testing
# ==================================================================


def make_aware(date_time: datetime):
    return timezone.make_aware(
        date_time,
        timezone=pytz.timezone(settings.TIME_ZONE),
    )


class TDDTest(TestCase):
    def setUp(self) -> None:
        self.user_birthday = date(1999, 3, 22)

    @expectedFailure
    def test_is_adult_step_1(self):
        with self.subTest("Il 21 marzo 2017 un secondo prima della mezzanotte non è maggiorenne"):
            with freeze_time(make_aware(datetime(2017, 3, 21, 23, 59, 59))):
                out = is_adult_step_1(self.user_birthday)
                self.assertFalse(out)

        with self.subTest("Il 22 marzo 2017 a mezzanotte è maggiorenne"):
            with freeze_time(make_aware(datetime(2017, 3, 22, 0, 0, 0))):
                out = is_adult_step_1(self.user_birthday)
                self.assertTrue(out)

    def test_is_adult_step_2(self):
        with self.subTest("Il 21 marzo 2017 un secondo prima della mezzanotte non è maggiorenne"):
            with freeze_time(make_aware(datetime(2017, 3, 21, 23, 59, 59))):
                out = is_adult_step_2(self.user_birthday)
                self.assertFalse(out)

        with self.subTest("Il 22 marzo 2017 a mezzanotte è maggiorenne"):
            with freeze_time(make_aware(datetime(2017, 3, 22, 0, 0, 0))):
                out = is_adult_step_2(self.user_birthday)
                self.assertTrue(out)
