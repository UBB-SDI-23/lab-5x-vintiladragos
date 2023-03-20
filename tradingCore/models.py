from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import UniqueConstraint

from .validators import GreaterThanValidator


class Stock(models.Model):
    symbol_name = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=100)
    dividend_yield = models.DecimalField(decimal_places=2, max_digits=4, default=0)
    price = models.DecimalField(decimal_places=2, max_digits=12)
    market_cap = models.PositiveBigIntegerField()

    def __str__(self):
        return self.symbol_name


class Trader(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    balance = models.DecimalField(decimal_places=2, max_digits=12, validators=[MinValueValidator(0)])
    net_p_and_l = models.DecimalField(decimal_places=2, max_digits=12, default=0, blank=True)
    mail = models.EmailField(max_length=100, unique=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Transaction(models.Model):
    trader_id = models.ForeignKey(Trader, on_delete=models.SET(None), blank=False)
    datetime = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[GreaterThanValidator(0)])
    type = models.CharField(max_length=10, choices=[("deposit", "deposit"), ('withdrawal', 'withdrawal')])

    def __str__(self):
        return self.trader_id.first_name + " " + self.trader_id.last_name + " " + str(self.amount) + " " + self.type


class TraderOwnedStock(models.Model):
    trader_id = models.ForeignKey(Trader, on_delete=models.CASCADE)
    stock_symbol = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        constraints = [UniqueConstraint(fields=['trader_id', 'stock_symbol'], name='unique_trader_stock')]

    def __str__(self):
        return self.trader_id.first_name + " " + self.trader_id.last_name + " " + self.stock_symbol.symbol_name + " " \
               + str(self.amount)



