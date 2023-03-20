from rest_framework import serializers
from tradingCore.models import *


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['symbol_name', 'full_name', 'dividend_yield', 'price', 'market_cap']


class StockPKSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['symbol_name']


class TraderPKSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trader
        fields = ['id']


class TransactionPKSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'trader_id', 'datetime', 'amount', 'type']


class TraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trader
        fields = ['id', 'first_name', 'last_name', 'balance', 'net_p_and_l', 'mail']


class TraderOwnedStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraderOwnedStock
        fields = ['id', 'trader_id', 'stock_symbol', 'amount']

