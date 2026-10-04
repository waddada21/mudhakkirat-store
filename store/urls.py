from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('order/<int:mudhakkira_id>/', views.order_create, name='order_create'),
    path('order/success/', views.order_success, name='order_success'),
]