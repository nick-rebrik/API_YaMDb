import datetime

from django.core.exceptions import ValidationError


def validator_year(val):
    current_year = datetime.date.today().year
    if val > current_year:
        raise ValidationError('Не может быть года из будущего')
    elif val < 1895:
        raise ValidationError('Тогда еще не было кинематографа')
