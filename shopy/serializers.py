from rest_framework import serializers
from shopy.models import Reserved, Account, Product


class ReserverSerializer(serializers.ModelSerializer):
    product_id = serializers.StringRelatedField()
    class Meta:
        model = Reserved
        fields = ('user', 'number_of_units', 'product_id')


class ProductSerializer(serializers.ModelSerializer):
    #product_id = serializers.StringRelatedField()
    class Meta:
        model = Product
        fields = ('name', 'shop_name', 'unit', 'number_of_units', 'price_for_unit', 'price_for_kg')


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('user', 'amount')

