from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("catalog/", include('apps.catalog.urls')),
    path('wishlist/', include('apps.wishlist.urls')),
    path('cart/', include('apps.cart.urls')),
    path('order/', include('apps.orders.urls')),
    path('newsletter/', include('apps.newsletter.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)