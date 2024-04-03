from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from counter.views import counter_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', counter_view),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
