from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    start_date = models.DateField()
    start_time = models.TimeField()
    max_students_per_group = models.PositiveIntegerField()
    min_students_per_group = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    video_link = models.URLField()

    def __str__(self):
        return self.title


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    paid = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

