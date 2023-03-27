from django.test import TestCase
from tradingCore.models import *


class MostExpensiveHoldingOfTrader(TestCase):
    def setUp(cls):
        pass
        Stock.objects.create(symbol_name='AAPL', full_name='Apple Inc.', dividend_yield=0.01, price=100, market_cap=100000000000)
        Stock.objects.create(symbol_name='MSFT', full_name='Microsoft Inc.', dividend_yield=0.01, price=100, market_cap=100000000000)
        Stock.objects.create(symbol_name='GOOG', full_name='Google Inc.', dividend_yield=0.01, price=100, market_cap=100000000000)
        Trader.objects.create(first_name='John', last_name='Doe', balance=100000, net_p_and_l=0)
        TraderOwnedStock.objects.create(trader_id=Trader.objects.get(first_name='John'), stock_symbol=Stock.objects.get(symbol_name='AAPL'), amount=100)
        TraderOwnedStock.objects.create(trader_id=Trader.objects.get(first_name='John'), stock_symbol=Stock.objects.get(symbol_name='MSFT'), amount=200)
        TraderOwnedStock.objects.create(trader_id=Trader.objects.get(first_name='John'), stock_symbol=Stock.objects.get(symbol_name='GOOG'), amount=150)

    def test_most_expensive_holding_of_trader(self):
        print(f'/most-expensive-holding-of-trader/{Trader.objects.get(first_name="John").id}')
        response = self.client.get(f'/most-expensive-holding-of-trader/{Trader.objects.get(first_name="John").id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['stock_symbol__symbol_name'], 'MSFT')

    def tearDown(cls):
        Stock.objects.all().delete()
        Trader.objects.all().delete()
        TraderOwnedStock.objects.all().delete()

class MostValuableStockHoldings(TestCase):
    def setUp(cls):
        pass
        Stock.objects.create(symbol_name='AAPL', full_name='Apple Inc.', dividend_yield=0.01, price=100, market_cap=100000000000)
        Stock.objects.create(symbol_name='MSFT', full_name='Microsoft Inc.', dividend_yield=0.01, price=100, market_cap=100000000000)
        Stock.objects.create(symbol_name='GOOG', full_name='Google Inc.', dividend_yield=0.01, price=100, market_cap=100000000000)
        Trader.objects.create(first_name='John', last_name='Doe', mail="asdf@gmail.com", balance=100000, net_p_and_l=0)
        Trader.objects.create(first_name='Jane', last_name='Doe', mail="asdff@gmail.com", balance=100000, net_p_and_l=0)
        TraderOwnedStock.objects.create(trader_id=Trader.objects.get(first_name='John'), stock_symbol=Stock.objects.get(symbol_name='AAPL'), amount=100)
        TraderOwnedStock.objects.create(trader_id=Trader.objects.get(first_name='John'), stock_symbol=Stock.objects.get(symbol_name='MSFT'), amount=200)
        TraderOwnedStock.objects.create(trader_id=Trader.objects.get(first_name='John'), stock_symbol=Stock.objects.get(symbol_name='GOOG'), amount=150)
        TraderOwnedStock.objects.create(trader_id=Trader.objects.get(first_name='Jane'), stock_symbol=Stock.objects.get(symbol_name='AAPL'), amount=300)
    def test_most_valuable_stock_holdings(self):
        print('/most-valuable-stock-holdings/')
        response = self.client.get('/most-valuable-stock-holdings/')
        self.assertEqual(response.status_code, 200)
        print(response.json())
        self.assertEqual(response.json()[0]['trader_id__first_name'], 'Jane')
        self.assertEqual(response.json()[1]['trader_id__first_name'], 'John')

    def tearDown(cls):
        Stock.objects.all().delete()
        Trader.objects.all().delete()
        TraderOwnedStock.objects.all().delete()