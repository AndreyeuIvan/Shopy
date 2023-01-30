from rest_framework import serializers
from shopy.models import Reserved, Account, Product

"""
class ReserverSerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedIdentityField(
        view_name='product-detail'
    )
    product = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    class Meta:
        model = Reserved
        fields = ('user', 'number_of_units', 'product')
"""


class ReserverSerializer(serializers.ModelSerializer):
    """
    product = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )"""

    def validate(self, value_data):
        validated_data = super().validate(value_data)
        print(self.context, "validate")
        #import pdb;pdb.set_trace()
        return validated_data
        raise serializers.ValidationError("ARRR")

    def validate_number_of_units(self, data):
        required_qty = self.initial_data["number_of_units"]
        try:
            if self.context['own_stock'] < required_qty:
                raise serializers.ValidationError("ARRR")
        except Exception:
            raise serializers.ValidationError("Except")
        validated_data = super().validate(data)
        return validated_data

    class Meta:
        model = Reserved
        fields = ("number_of_units", "product")


class ProductSerializer(serializers.ModelSerializer):
    reverse = ReserverSerializer(many=True)
    """
    def validate(self, own_stock, required_qty):
        import pdb;pdb.set_trace()
        if own_stock.number_of_units < required_qty:
            raise serializers.ValidationError('ARRR')
    """

    def create(self, validated_data):
        reverses_data = validated_data.pop("reverse")
        product = Product.objects.create(**validated_data)
        for reverse_data in reverses_data:
            Reserved.objects.create(product=product, **reverse_data)
        return product

    class Meta:
        model = Product
        fields = ("id", "name", "reverse")


class AccountSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Account
        fields = ("user", "amount")
        
    def validate(self, data):
        print(data)
        #import pdb;pdb.set_trace()
        user_amount = Account.objects.get(user=self.context['user']).amount
        if user_amount < self.context['sum_reserved']:
            raise serializers.ValidationError('Fullfill your account')
        validated_data = super().validate(data)
        return validated_data
