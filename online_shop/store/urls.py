from django.urls import path
from .views import CartDetailAndAddView, CartItemUpdateDeleteView

urlpatterns = [
    path('cart/', CartDetailAndAddView.as_view(), name='cart-detail-add'),
    path('cart/items/<int:pk>/', CartItemUpdateDeleteView.as_view(), name='cart-item-update-delete'),
]