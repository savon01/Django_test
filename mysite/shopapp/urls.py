from django.urls import path

from .views import ProductListView, RegisterView
from .api import ProductListAPIView, StudentLessonsView, ProductStatsAPIView


app_name = 'shopapp'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('register/<int:product_id>/', RegisterView.as_view(), name='register'),
    path('api/products/', ProductListAPIView.as_view(), name='product_list_api'),
    path('api/students/<str:phone>/lessons/', StudentLessonsView.as_view(), name='student-lessons'),
    path('api/products_stat/', ProductStatsAPIView.as_view(), name='product-stats')
]
