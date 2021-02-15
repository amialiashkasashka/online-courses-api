from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .permissions import (
    IsTeacher, IsCreatorOrReadOnly,
    IsStudentOrTeacher, IsStudent
)
from .serializers import (
    UserRegistrationSerializer, CourseListSerializer,
    CourseDetailSerializer, CourseParticipantSerializer,
    ParticipantDeleteSerializer, LectureListSerializer,
    LectureDetailSerializer, HomeworkSerializer,
    HomeworkCreateSerializer, MarkSerializer,
    CommentSerializer, SolutionSerializer,
    ListParticipantSerializer
)
from .models import (
    Homework, Comment, Solution,
    Course, Mark, Lecture
)

User = get_user_model()



class UserRegisterView(generics.CreateAPIView):
    '''
    API endpoint to create new user
    '''
    # permission_classes =IsNotAuthenticated
    serializer_class = UserRegistrationSerializer


class CourseViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows to crud course
    '''
    serializer_class = CourseListSerializer

    def get_queryset(self):
        '''
        for teacher returns courses where he teaches, for students where they are participants
        :return:
        '''
        user = self.request.user
        if user.role == 'teacher':
            try:
                return Course.objects.all().filter(user=user.id)
            except ObjectDoesNotExist:
                raise Http404
        elif user.role == 'student':
            return Course.objects.filter(user__in=Course.participants)

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PUT']:
            self.permission_classes = [IsAuthenticated, IsTeacher,]
        else:
            self.permission_classes = [IsAuthenticated, IsStudentOrTeacher,]
        return super(CourseViewSet, self).get_permissions()


class HandleParticipantViewSet(viewsets.ModelViewSet):
    '''
    API endpoint that allows teachers to add/remove and to read if you are a student
    '''
    http_method_names = ['put', 'delete', 'get']

    def update(self, request, *args, **kwargs):
        serializer = CourseParticipantSerializer(data=self.request.data)
        if serializer.is_valid():
            course = Course.objects.get(id=self.kwargs['course_id'])
            user = User.objects.get(id=serializer.validated_data['user_id'])
            if user is not None:
                course.participants.add(user)
                return Response({}, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        serializer = ParticipantDeleteSerializer(data=self.request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, id=serializer.validated_data['user_id'])
            course = get_object_or_404(Course, id=self.kwargs['course_id'])
            course.participants.remove(user)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        '''
        returns only students of the current course
        :return:
        '''
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return course.participants.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PUT']:
            self.permission_classes = [IsAuthenticated, IsTeacher,]
        else:
            self.permission_classes = [IsAuthenticated, IsStudentOrTeacher,]
        return super(HandleParticipantViewSet, self).get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            self.serializer_class = ListParticipantSerializer
        elif self.request.method == 'DELETE':
            self.serializer_class = ParticipantDeleteSerializer
        else:
            self.serializer_class = CourseParticipantSerializer
        return super(HandleParticipantViewSet, self).get_serializer_class()


class LectureCreateView(generics.CreateAPIView):
    '''
    API endpoint that allows teachers to create lectures
    '''
    permission_classes = (IsAuthenticated, IsTeacher,)
    serializer_class = LectureListSerializer


class LectureDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    API endpoint that allows teachers to edit lecture
    '''
    permission_classes = (IsAuthenticated, IsTeacher,)
    serializer_class = LectureDetailSerializer
    queryset = Lecture.objects.all()


class LectureListView(generics.ListAPIView):
    '''
    API endpoint that allows current course participants to get
    the list of lectures of the course
    '''
    permission_classes = (IsAuthenticated, IsStudentOrTeacher,)
    serializer_class = LectureListSerializer

    def get_queryset(self):
        user = self.request.user
        course = Course.objects.get(id=self.kwargs['course_id'])
        if user in course.participants.all():
            return Lecture.objects.all().filter(course=self.kwargs['course_id'])


class HomeworkListView(generics.ListAPIView):
    '''
    API endpoint that allows to get homework of current lecture
    '''
    permission_classes = (IsAuthenticated, IsStudentOrTeacher,)
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        return Homework.objects.filter(lecture=self.kwargs['pk'])


class HomeworkDoneView(generics.ListAPIView):
    '''
    API endpoint that allows teachers to see finished homeworks
    to rate their solutions
    '''
    permission_classes = (IsAuthenticated, IsTeacher,)
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        return Homework.objects.all().filter(has_done=True)


class HomeworkCreateView(generics.CreateAPIView):
    '''
    API endpoint that allows teachers to create homework for each lecture
    '''
    permission_classes = (IsAuthenticated, IsTeacher,)
    serializer_class = HomeworkCreateSerializer


class SolutionCreateView(viewsets.ModelViewSet):
    '''
    API endpoint that updates `has_done` field in homework model right
    after solution being created
    '''
    permission_classes = (IsAuthenticated, IsStudent,)
    serializer_class = SolutionSerializer

    def perform_create(self, serializer):
        _solution = Solution.objects.create(
            student = serializer.validated_data['student'],
            homework = serializer.validated_data['homework'],
            solution = serializer.validated_data['solution']
        )
        Homework.objects.filter(id=_solution.homework.id).update(has_done=True)
        serializer.save()


class SolutionListView(generics.ListAPIView):
    '''
    API endpoint to view user`s solution
    '''
    permission_classes = (IsAuthenticated, IsStudentOrTeacher,)
    serializer_class = SolutionSerializer

    def get_queryset(self):
        return Solution.objects.filter(student=self.request.user.id)

class MarkCreateView(generics.CreateAPIView):
    """
    API endpoint that allows teachers to rate homework`s solution
    """
    permission_classes = (IsAuthenticated, IsTeacher,)
    serializer_class = MarkSerializer


class MarkListView(generics.ListAPIView):
    """
    API endpoint that allows students to see their marks, teachers too
    """
    permission_classes = (IsAuthenticated, IsStudentOrTeacher,)
    serializer_class = MarkSerializer

    def get_queryset(self):
        return Mark.objects.filter(solution__student=self.request.user)


class MarkDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows teachers to edit marks
    """

    permission_classes = (IsAuthenticated, IsTeacher,)
    serializer_class = MarkSerializer

    def get_queryset(self):
        return Mark.objects.filter(id=self.kwargs['pk'])


class CommentCreateView(generics.CreateAPIView):
    """
    API endpoint that allows students/teachers to comment marks
    """

    permission_classes = (IsAuthenticated, IsStudentOrTeacher)
    serializer_class = CommentSerializer

class CommentListView(generics.ListAPIView):
    """
    API endpoint that allows comments to be viewed
    """
    permission_classes = (IsAuthenticated, IsStudentOrTeacher)
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all().filter(mark=self.kwargs['mark_id'])






