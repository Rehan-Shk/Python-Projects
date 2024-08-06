from .models import MenuItems, Category
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class MenuItemsSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    # Method 1 for displaying nested fields
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

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

    def calculate_tax(self, product:MenuItems):
        return (product.price * Decimal(0.15)) + product.price
