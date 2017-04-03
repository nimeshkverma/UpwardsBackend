from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('social.urls')),
    url(r'^', include('eligibility.urls')),
    url(r'^', include('customer.urls')),
    url(r'^', include('pan.urls')),
    url(r'^', include('aadhaar.urls')),
    url(r'^customer/', include('common.urls')),
    url(r'^customer/', include('messenger.urls')),
    url(r'^customer/', include('activity.urls')),
    url(r'^customer/', include('documents.urls')),
    url(r'^common/', include('common.urls')),
    url(r'^participant/', include('participant.urls')),
    url(r'^loan/', include('loan.urls')),
    url(r'^transaction/', include('transaction.urls')),
    url(r'^analytics/', include('analytics.urls')),
    url(r'^third_party_leads/', include('thirdpartyleads.urls')),

]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
