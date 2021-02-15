
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .router import router



schema_view = get_schema_view(
   openapi.Info(
      title="online-courses-api",
      default_version='v1',
      description="online-courses-api project, made with django/drf, authentication on drf-simplejwt, documented with drf-yasg ",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="a.amialiashka@gmail.com"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('api/v1/', include('main_app.urls')),
    path('api/v1/', include(router.urls)),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]