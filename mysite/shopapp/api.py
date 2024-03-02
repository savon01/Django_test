from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Student
from .serializers import ProductSerializer, LessonSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StudentLessonsView(APIView):
    def get(self, request, phone):
        try:
            # Получаем студента по номеру телефона
            student = Student.objects.get(phone=phone)
            # Получаем продукт, к которому студент имеет доступ
            product = student.group.product
            # Получаем все уроки для этого продукта
            lessons = product.lessons.all()
            # Сериализуем уроки и возвращаем их
            serializer = LessonSerializer(lessons, many=True)
            return Response(serializer.data)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
