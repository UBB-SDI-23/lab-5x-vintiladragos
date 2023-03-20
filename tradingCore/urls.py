from django.urls import path

from tradingCore import views

urlpatterns = [
    path('stocks/', views.stock_list),
    path('stocks/<str:symbol_name>', views.stock_detail),
    path('traders/', views.trader_list),
    path('traders/<int:pk>', views.trader_detail),
    path('traders/<int:trader_id>/stocks/', views.trader_owned_stock_list),
    path('traders/<int:trader_id>/stocks/<str:symbol_name>', views.trader_owned_stock_detail),
    path('traders/<int:pk>/transactions/', views.transaction_list),
    path('traders/balance-higher-than/<int:number>', views.trader_balance_higher_than),
    path('transactions/', views.transaction_list_all),
    path('transactions/<int:pk>', views.transaction_detail),
    path('trader-owned-stocks/', views.trader_owned_stock_list_all),
    path('most-valuable-stock-holdings/', views.most_valuable_stock_holdings),
    path('most-expensive-holding-of-trader/<int:trader_id>', views.most_expensive_holding_of_trader),
]

