from django.shortcuts import render
from shop.models import Product, Review
from rest_framework import views
from rest_framework.response import Response
from .serializers import ProductSerializer


class ProductsApiView(views.APIView):
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class ProductApiView(views.APIView):

    def get(self, requset, pk):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
