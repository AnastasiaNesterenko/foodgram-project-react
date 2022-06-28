from django.core.validators import RegexValidator

characters_validator = RegexValidator(
    r'^[-a-zA-Z0-9_]+$',
    'Символы латинского алфавита, цифры и знак подчёркивания'
)
