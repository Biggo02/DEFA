from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

from core.views import ApplicationViewSet, health, me
from core.payment_api import collect_payment

application_list = ApplicationViewSet.as_view({'get': 'list', 'post': 'create'})

urlpatterns = [
    path('admin/', admin.site.urls),

    # Canonical API namespace.
    path('api/', include('core.urls')),

    # Backward-compatible API endpoints kept at the root for existing clients/tests.
    path('health/', health, name='api-health-root'),
    path('me/', me, name='api-me-root'),
    path('applications/', application_list, name='api-applications-root'),
    path('payments/collect/', collect_payment, name='api-payment-collect-root'),

    # Django-rendered frontend.
    path('', include('core.web_urls')),
]

handler404 = 'config.urls.error_404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def error_404(request, exception):
    return render(request, '404.html', status=404)
