from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MenuItems, Category
from .serializers import MenuItemsSerializer, CategorySerializer
from django.core.paginator import Paginator, EmptyPage
from rest_framework.throttling import AnonRateThrottle


class MenuItemView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle]
    permission_classes = [IsAuthenticated]
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemsSerializer

    def get_queryset(self):
        query_set = MenuItems.objects.all()
        category_title = self.request.query_params.get('category', None)
        price = self.request.query_params.get('price', None)
        search = self.request.query_params.get('search', None)
        ordering = self.request.query_params.get('ordering', None)
        per_page = self.request.query_params.get('per-page', default=2)
        page = self.request.query_params.get('page', default=1)
        if category_title:
            query_set = query_set.filter(category__title=category_title)
        if price:
            query_set = query_set.filter(price__lte=price)
        if search:
            query_set = query_set.filter(title__icontains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            query_set = query_set.order_by(*ordering_fields)

        paginator = Paginator(query_set, per_page=per_page)
        try:
            query_set = paginator.page(number=page)
        except EmptyPage:
            query_set = []

        return query_set


class SingleMenuItem(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemsSerializer


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@api_view()
@permission_classes([IsAuthenticated])
def secret_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({'message': 'Secret View'})
    else:
        return Response({'message': 'You are not authorized'}, 403)


@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({'message': 'Successfull'})
