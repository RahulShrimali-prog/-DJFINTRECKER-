from django.contrib import admin
from django.urls import path
from finance.views import registerView, dashboardview, TransectioncreateView,Transactionlistview,GoalView,export_transactions

urlpatterns = [
    path('register/', registerView.as_view(), name='register'),  # Register view
    path('', dashboardview.as_view(), name='dashboard'),  # Dashboard view
    path('transection/Add/', TransectioncreateView.as_view(), name='transection_Add'),  # Transaction create view
    path('Transaction', Transactionlistview.as_view(), name='Transaction'),
    path('Goal/add/', GoalView.as_view(), name="Goal_add"),
    path('generate-report/', export_transactions, name='export_transactions') 
]