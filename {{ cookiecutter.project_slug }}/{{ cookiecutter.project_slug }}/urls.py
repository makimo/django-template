from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', include('{{ cookiecutter.project_slug }}.apps.hello_world.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Debug Toolbar.
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
