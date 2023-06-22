from django.urls import path
from shop.views import ProductApiView,ProductsApiView

urlpatterns = [
    path('products/', ProductsApiView.as_view(), name='products'),
    path('products/<str:pk>/', ProductApiView.as_view(), name='product')
]