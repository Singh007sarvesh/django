from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    joining_date = models.DateTimeField(auto_now_add=True)
    course = models.CharField(max_length=100, blank=True, default='')
    department = models.CharField(max_length=100, blank=True, default='')
