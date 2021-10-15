from django.contrib import admin
from django.urls import path, include
from products.views import HomeView
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, logout_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('profile/', include('profiles.urls', namespace='profiles')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('sales/', include('sales.urls', namespace='sales')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]



urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)