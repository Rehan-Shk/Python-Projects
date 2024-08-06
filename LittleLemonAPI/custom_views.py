from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import MenuItems, Category
from .serializers import MenuItemsSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework import status


# Create your views here.
@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItems.objects.select_related('category').all()
        serialized_items = MenuItemsSerializer(items, many=True, context={'request': request})
        return Response(serialized_items.data)
    elif request.method == 'POST':
        serialized_items = MenuItemsSerializer(data=request.data)
        serialized_items.is_valid(raise_exception=True)
        serialized_items.save()
        return Response(serialized_items.data, status.HTTP_201_CREATED)


@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItems, pk=id)
    serialized_item = MenuItemsSerializer(item)
    return Response(serialized_item.data)


@api_view(['GET', 'POST'])
def category_detail(request, pk):
    if request.method == 'POST':
        serialized_data = CategorySerializer(data=request.data)
        serialized_data.is_valid(raise_exception=True)
        serialized_data.save()
        return Response(serialized_data.data, status.HTTP_201_CREATED)
    if request.method == 'GET':
        category = get_object_or_404(Category, pk=pk)
        serialized_data = CategorySerializer(category)
        return Response(serialized_data.data, status.HTTP_200_OK)
