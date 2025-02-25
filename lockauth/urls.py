from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import homepage  # ✅ استيراد الصفحة الرئيسية

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', homepage, name='homepage'),  # ✅ جعل الصفحة الرئيسية `/`
]

# ✅ إجبار Django على تقديم الملفات الإعلامية حتى في بيئة الإنتاج
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
