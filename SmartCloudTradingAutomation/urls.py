from django.urls import path, include
from django.contrib import admin

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view (
   openapi.Info(
      title="Smart Cloud Trading Automation API",
      default_version='v1',
      description="API documentation for Smart Cloud Trading Automation",
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('trading.urls')),

    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
