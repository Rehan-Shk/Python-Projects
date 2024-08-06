from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items', views.MenuItemView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>', views.SingleMenuItem.as_view()),
    path('category', views.CategoryView.as_view(), name='category-detail'),
    path('category/<int:pk>', views.SingleCategoryView.as_view(), name='category-detail'),
    path('secret', views.secret_view),
    path('api-token-auth', obtain_auth_token),
    path('throttle-check', views.throttle_check)
]