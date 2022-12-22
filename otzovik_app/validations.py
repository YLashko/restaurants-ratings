from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from otzovik_app.config import EMAIL_REGEX_PATTERN


def validate_username(username: str):
    if len(username) < 3:
        raise ValidationError(_("Username is too short"))


def validate_email(email: str):
    if not EMAIL_REGEX_PATTERN.match(email):
        raise ValidationError(_('Invalid email'))


def validate_restaurant_name(restaurant_name: str):
    if len(restaurant_name) < 4:
        raise ValidationError(_('Restaurant name is too short'))
