from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Stock(models.Model):
    full_name = models.CharField(max_length=100)
    symbol_name = models.CharField(max_length=10, unique=True)
    dividend_yield = models.DecimalField(decimal_places=2, max_digits=4, default=0)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    market_cap = models.PositiveBigIntegerField()

    def __str__(self):
        return self.symbol_name

