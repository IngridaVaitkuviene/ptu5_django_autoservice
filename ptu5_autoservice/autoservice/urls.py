from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('car/<int:car_id>/', views.car_info, name='car_info'),
    path('orders/', views.OrderlistView.as_view(), name='orders'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order'),
    path('my_orders/', views.UserOrderListView.as_view(), name='user_orders'),
    path('create_new_order/', views.UserOrderCreateView.as_view(), name='user_order_create'),
    path('update_order/<int:pk>/', views.UserOrderUpdateView.as_view(), name='user_order_update'),
    path('cancel_order/<int:pk>/', views.UserOrderDeleteView.as_view(), name='user_order_delete'),
]
