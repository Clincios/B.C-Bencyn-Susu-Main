"""
URL configuration for bencyn_susu project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.admin_views import about_settings_view

urlpatterns = [
    # Custom admin views must come BEFORE admin.site.urls to avoid catch-all pattern
    path('admin/about-settings/', about_settings_view, name='about_settings'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# Media files (user uploads) - only served in DEBUG mode
# In production, serve media files through your web server (nginx, Apache, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Static files are now served by WhiteNoise in production
# No need for static() URL pattern - WhiteNoise middleware handles it
