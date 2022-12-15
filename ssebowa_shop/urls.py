from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = "Ssebowa"
admin.site.site_title = "ssebowa admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('shop.urls')),
    path('auth/',include('authentication.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

MID=" " #murchnet ID
MK=" " # muschint Key