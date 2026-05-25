from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url='/vacancies/')),
    path('admin/',      admin.site.urls),
    path('accounts/',   include('apps.accounts.urls')),
    path('applicants/', include('apps.applicants.urls')),
    path('employers/',  include('apps.employers.urls')),
    path('vacancies/',  include('apps.vacancies.urls')),
    path('payments/',   include('apps.payments.urls')),
    path('dashboard/',  include('apps.dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
