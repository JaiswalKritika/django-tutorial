from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    path('homepage/', views.homepage, name='homepage'),
    path('quick_view/', views.quick_view, name='quick_view'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('carts/', views.cart, name='carts'),
    path('remove_cart/<int:cart_id>/', views.remove_cart, name='remove_cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('product/', views.product, name='product'),
    path('shop/', views.shop, name='shop'),
    path('checkout/', views.checkout, name='checkout'),
    path('custom/', views.custom, name='custom'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('get_filter/', views.get_filters, name='get_filter'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('activate_email/<email_token>', views.activate_email, name='activate_email'),

]