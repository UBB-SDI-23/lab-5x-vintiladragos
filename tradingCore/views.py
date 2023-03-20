from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.db.models import F, Sum
from tradingCore.models import *
from tradingCore.serializers import *
from rest_framework import viewsets
from rest_framework import permissions


@csrf_exempt
def trader_balance_higher_than(request, number):
    if request.method == 'GET':
        traders = Trader.objects.filter(balance__gt=number)
        serializer = TraderSerializer(traders, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def trader_list(request):
    """
    List all traders, or add a new trader.
    """
    if request.method == 'GET':
        traders = Trader.objects.values('id')
        serializer = TraderPKSerializer(traders, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TraderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def trader_detail(request, pk):
    """
    Retrieve, update or delete a trader.
    """
    try:
        trader = Trader.objects.get(pk=pk)
    except Trader.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TraderSerializer(trader)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TraderSerializer(trader, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        trader.delete()
        return HttpResponse(status=204)


@csrf_exempt
def stock_list(request):
    """
    List all stocks, or add a new stock.
    """
    if request.method == 'GET':
        stocks = Stock.objects.values('symbol_name')
        serializer = StockPKSerializer(stocks, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StockSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def stock_detail(request, symbol_name):
    """
    Retrieve, update or delete a stock.
    """
    try:
        stock = Stock.objects.get(symbol_name=symbol_name)
    except Stock.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = StockSerializer(stock)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = StockSerializer(stock, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        stock.delete()
        return HttpResponse(status=204)


@csrf_exempt
def transaction_list_all(request):
    """
    List all transactions
    """
    if request.method == 'GET':
        transactions = Transaction.objects.values('id')
        serializer = TransactionPKSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def transaction_list(request, pk):
    """
    List transactions from a trader, or add a new transaction to that trader with trader id = pk.
    """
    if request.method == 'GET':
        transactions = Transaction.objects.filter(trader_id=pk)
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['trader_id'] = pk
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            amount = serializer.initial_data['amount']
            if serializer.initial_data['type'] == 'deposit':
                Trader.objects.filter(pk=pk).update(balance=F('balance') + amount)
            else:
                Trader.objects.filter(pk=pk).update(balance=F('balance') - amount)
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def transaction_detail(request, pk):
    """
    Retrieve, update or delete a transaction.
    """

    try:
        transaction = Transaction.objects.get(pk=pk)
    except Stock.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(transaction, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        transaction.delete()
        return HttpResponse(status=204)


@csrf_exempt
def trader_owned_stock_list_all(request):
    """
    List all stocks owned by all traders
    """
    if request.method == 'GET':
        owned_stocks = TraderOwnedStock.objects.all()
        serializer = TraderOwnedStockSerializer(owned_stocks, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def trader_owned_stock_list(request, trader_id):
    """
    List all trader owned stocks, or add a new trader owned stock.
    """
    if request.method == 'GET':
        owned_stocks = TraderOwnedStock.objects.filter(trader_id=trader_id)
        serializer = TraderOwnedStockSerializer(owned_stocks, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['trader_id'] = trader_id
        serializer = TraderOwnedStockSerializer(data=data)
        if serializer.is_valid():
            try:
                TraderOwnedStock.objects.get(trader_id=serializer.initial_data['trader_id'], stock_symbol=serializer.initial_data['stock_symbol'])
            except TraderOwnedStock.DoesNotExist:
                serializer.save()
            else:
                TraderOwnedStock.objects.update(trader_id=serializer.initial_data['trader_id'],
                                                stock_symbol=serializer.initial_data['stock_symbol'],
                                                amount=serializer.initial_data['amount'])
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def trader_owned_stock_detail(request, trader_id, symbol_name):
    """
    Retrieve, update or delete a trader owned stock.
    """
    try:
        trader_owned_stock = TraderOwnedStock.objects.get(trader_id=trader_id, stock_symbol=symbol_name)
    except TraderOwnedStock.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TraderOwnedStockSerializer(trader_owned_stock)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        data["stock_symbol"] = symbol_name
        data["trader_id"] = trader_id
        serializer = TraderOwnedStockSerializer(trader_owned_stock, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        trader_owned_stock.delete()
        return HttpResponse(status=204)


def most_valuable_stock_holdings(request):
    """
    List all traders ordered by portofolio value
    """
    if request.method == 'GET':
        queryset = TraderOwnedStock.objects.select_related('trader', 'stock')\
            .annotate(value=F('amount') * F('stock_symbol__price'))\
            .order_by('-value')\
            .values('trader_id__first_name', 'trader_id__last_name', 'value')
        data = list(queryset)
        return JsonResponse(data, safe=False)


def most_expensive_holding_of_trader(request, trader_id):
    """
    List most expensive stock holding of a trader
    """

    if request.method == 'GET':
        queryset = TraderOwnedStock.objects\
            .select_related('trader_id')\
            .filter(trader_id=trader_id)\
            .annotate(value=F('amount') * F('stock_symbol__price'))\
            .values('stock_symbol__symbol_name', 'value', 'amount')\
            .order_by('-value')\
            .first()

        return JsonResponse(queryset, safe=False)
