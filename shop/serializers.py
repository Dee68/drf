from rest_framework import serializers
from shop.models import Product, Review


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields ='__all__'