from django.urls import path
from .views import (
    UserRegisterView, LectureDetailView,
    LectureCreateView, LectureListView, CommentListView,
    CommentCreateView, HomeworkListView,
    HomeworkCreateView, HomeworkDoneView, MarkListView,
    MarkCreateView, MarkDetailView, SolutionCreateView,
    SolutionListView, HandleParticipantViewSet
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # course urls
    path('courses/<int:course_id>/students/', HandleParticipantViewSet.as_view({'put': 'update',
                                                                                'delete': 'destroy',
                                                                                'get': 'list'})),
    # lecture urls
    path('lecture/detail/<int:pk>/', LectureDetailView.as_view()),
    path('courses/<int:course_id>/lectures/create/', LectureCreateView.as_view()),
    path('courses/<int:course_id>/lectures/all/', LectureListView.as_view()),

    # homework urls
    path('lecture/<int:pk>/homework/create/', HomeworkCreateView.as_view()),
    path('lecture/<int:pk>/homework/', HomeworkListView.as_view()),
    path('homeworks/done/', HomeworkDoneView.as_view()),

    # solution homework urls
    path('solutions/solution/create/', SolutionCreateView.as_view({'post': 'create'})),
    path('solutions/all/', SolutionListView.as_view()),

    # mark urls
    path('marks/mark/create/', MarkCreateView.as_view()),
    path('marks/all/', MarkListView.as_view()),
    path('marks/<int:pk>/', MarkDetailView.as_view()),

    # comments urls
    path('marks/mark/<int:mark_id>/comments/', CommentListView.as_view()),
    path('marks/mark/<int:mark_id>/comments/create/', CommentCreateView.as_view()),

    path('users/create/', UserRegisterView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
