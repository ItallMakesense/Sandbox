from django.core.exceptions import ValidationError


def validate_category(value):
    if value.lower() == 'forbidden':
        raise ValidationError(f'{value} is not a valid directory')
