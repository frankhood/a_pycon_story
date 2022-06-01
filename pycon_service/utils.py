import datetime

from dateutil.relativedelta import relativedelta
from django.utils import timezone


def is_adult_step_1(birth_date: datetime.date) -> bool:
    if birth_date <= (timezone.now() - relativedelta(years=18)).date():
        return True
    return False


def is_adult_step_2(birth_date: datetime.date) -> bool:
    if birth_date <= (timezone.localtime(timezone.now()) - relativedelta(years=18)).date():
        return True
    return False
