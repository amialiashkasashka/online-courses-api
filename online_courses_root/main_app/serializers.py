from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            role = validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'password')

class CourseListSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = '__all__'

class CourseDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

class CourseParticipantSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id', 'user_id', 'role',)

class ListParticipantSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'role')


class ParticipantDeleteSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('id', 'user_id',)

class LectureListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecture
        fields = '__all__'

class LectureDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecture
        fields = ('id', 'title', 'file', 'course')


class HomeworkSerializer(serializers.ModelSerializer):

     class Meta:
        model = Homework
        fields = '__all__'

class HomeworkCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Homework
        fields = ('task', 'lecture',)

class SolutionSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Solution
        fields = '__all__'


class MarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mark
        fields = ('mark', 'solution',)

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('author', 'comment', 'mark')