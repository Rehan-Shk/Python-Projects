from .models import MenuItems, Category
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class MenuItemsSerializer(serializers.ModelSerializer):
    # Method 1 for validation
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    # stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # category = serializers.HyperlinkedIdentityField(view_name='category-detail', format='html')

    # Method 1 for displaying nested fields
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    # Method 2 for validation
    # def validate_price(self, value):
    #     if value < 2:
    #         raise serializers.ValidationError('Price should not be less than 2.0')

    class Meta:
        model = MenuItems
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
        extra_kwargs = {
            # Method 3 for validation
            'price': {'min_value': 2},
            'stock': {'min_value': 0, 'source': 'inventory'},
            'title': {
                'validators': [
                    UniqueValidator(
                        queryset=MenuItems.objects.all()
                    )
                ]
            }
        }
        # Method 2 for displaying nested fields
        # depth = 1

    def calculate_tax(self, product:MenuItems):
        return (product.price * Decimal(0.15)) + product.price
