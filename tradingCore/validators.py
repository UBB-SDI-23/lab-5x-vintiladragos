from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class GreaterThanValidator(MinValueValidator):
    message = _("Ensure this value is greater than %(limit_value)s.")
    code = "greater_than_value"

    def compare(self, a, b):
        return a <= b
