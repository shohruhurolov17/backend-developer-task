
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.views import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.common.urls')),
    path('api/v1/', include('apps.orders.urls')),
    path('api/v1/', include('apps.posts.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
]

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
# urlpatterns += [static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)]
