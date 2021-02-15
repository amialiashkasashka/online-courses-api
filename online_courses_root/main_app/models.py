from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class User(AbstractUser):

    ROLE = (
        ('student', 'student'),
        ('teacher', 'teacher')
    )

    role = models.CharField(max_length=20, choices=ROLE)
    email = models.EmailField(blank=False, unique=True)

    REQUIRED_FIELDS = ['email', 'role']


class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='course_participants', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users', null=True)

    def __str__(self):
        return self.title


class Lecture(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='uploads/lectures/', blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Homework(models.Model):
    task = models.TextField(blank=True, null=True)
    has_done = models.BooleanField(default=False)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True, related_name='_lecture')

    def __str__(self):
        return self.task


class Solution(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    homework = models.OneToOneField(Homework, on_delete=models.CASCADE, null=True)
    solution = models.TextField(blank=False)

    def __str__(self):
        return self.homework


class Mark(models.Model):
    mark = models.IntegerField(default=0, validators=[MaxValueValidator(10), MinValueValidator(0)])
    solution = models.OneToOneField(Solution, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Mark - {self.mark}'

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=200)
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.comment