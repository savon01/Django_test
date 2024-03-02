from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

from .views import ProductListView, RegisterView
from .api import ProductListAPIView, StudentLessonsView


app_name = 'shopapp'

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('register/<int:product_id>/', RegisterView.as_view(), name='register'),
    path('api/products/', ProductListAPIView.as_view(), name='product_list_api'),
    path('api/students/<str:phone>/lessons/', StudentLessonsView.as_view(), name='student-lessons'),
]
