from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from tradingCore.models import Stock
from tradingCore.serializers import StockSerializer
from rest_framework import viewsets
from rest_framework import permissions


class StockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows stocks to be viewed or edited.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # permission_classes = [permissions.IsAuthenticated]


@csrf_exempt
def stock_list(request):
    """
    List all stocks, or add a new stock.
    """
    if request.method == 'GET':
        snippets = Stock.objects.all()
        serializer = StockSerializer(snippets, many=True)
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

