from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create', views.acc_creation, name = 'create'),
    path('pin', views.pin_generate, name = 'pin'),
    path('validate', views.validation, name = 'valid'),
    path('balance', views.balance, name = 'balance'),
    path('withdraw', views.withdrawn, name = 'withdrawn'),
    path('deposite', views.deposite, name = 'deposite'),
    path('transfer', views.transfer, name = 'transfer'),
    path('transfer_validation',views.transfer_validation,name="transfer_validation"),
    path('delete',views.deletion,name="delete"),
    path('delete_validate',views.delete_validate,name="delete_validate")
]