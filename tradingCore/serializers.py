from rest_framework import serializers
from tradingCore.models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'symbol_name', 'full_name', 'dividend_yield', 'price', 'market_cap']
