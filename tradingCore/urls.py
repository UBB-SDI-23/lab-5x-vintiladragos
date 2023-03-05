from django.urls import path

from tradingCore import views

urlpatterns = [
    path('stocks/', views.stock_list),
    path('stocks/<str:symbol_name>', views.stock_detail)
]

