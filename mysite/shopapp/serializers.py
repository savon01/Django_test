from rest_framework import serializers
from .models import Product, Lesson, Student, Group


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_link']


class ProductSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'creator', 'start_date', 'start_time', 'max_students_per_group',
                  'min_students_per_group', 'lessons']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'phone', 'paid', 'group']


class GroupSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ['name', 'students']

