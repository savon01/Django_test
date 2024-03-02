from rest_framework import serializers
from django.db.models import Avg, Count

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


class ProductSerializerDop(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    groups_fill_percentage = serializers.SerializerMethodField()
    product_purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'creator', 'groups', 'lessons', 'students_count', 'groups_fill_percentage', 'product_purchase_percentage')

    def get_groups(self, obj):
        groups = obj.groups.all()
        return GroupSerializerDop(groups, many=True).data

    def get_lessons(self, obj):
        lessons = obj.lessons.all()
        return LessonSerializerDop(lessons, many=True).data

    def get_students_count(self, obj):
        return Student.objects.filter(group__product=obj).count()

    def get_groups_fill_percentage(self, obj):
        groups = Group.objects.filter(product=obj).annotate(students_count=Count('students'))
        if groups:
            max_students_per_group = obj.max_students_per_group
            average_fill_percentage = groups.aggregate(average=Avg('students_count'))['average']
            if average_fill_percentage and max_students_per_group:
                return round((average_fill_percentage / max_students_per_group) * 100, 2)
        return 0

    def get_product_purchase_percentage(self, obj):
        total_students_count = Student.objects.count()
        if total_students_count > 0:
            product_students_count = Student.objects.filter(group__product=obj).distinct().count()
            purchase_percentage = (product_students_count / total_students_count) * 100
            return round(purchase_percentage, 2)
        return 0


class GroupSerializerDop(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)

class LessonSerializerDop(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title', 'video_link')

