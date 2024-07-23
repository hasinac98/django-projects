from django.urls import path
from cart import views

app_name='cart'
urlpatterns = [
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('cart-view/',views.cart_view,name='cart_view'),
    path('cart_decrement/<int:id>',views.cart_decrement,name='cart_decrement'),
    path('cart_delete/<int:id>',views.cart_delete,name='cart_delete'),
    path('place_order/',views.place_order,name='place_order'),
    path('status/<u>',views.payment_status,name='status'),
    path('order_view/',views.order_view,name='order_view'),


]

