from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'tfaDemo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^tfa/', include('tfa.urls')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)