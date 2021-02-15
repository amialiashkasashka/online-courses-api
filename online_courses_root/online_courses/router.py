from rest_framework import routers
from main_app.views import CourseViewSet, HandleParticipantViewSet


router = routers.DefaultRouter()
router.register('courses', CourseViewSet, basename='course')
