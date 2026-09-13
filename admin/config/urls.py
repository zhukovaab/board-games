from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

admin.site.site_header = "Домашняя библиотека настолок"
admin.site.site_title = "Настолки"
admin.site.index_title = "Управление коллекцией"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("martor/", include("martor.urls")),
    path("", RedirectView.as_view(url="/admin/", permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
