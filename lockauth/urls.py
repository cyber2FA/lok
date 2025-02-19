from django.contrib import admin
from django.urls import path, include
from accounts.views import homepage  # ✅ استيراد الصفحة الرئيسية

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', homepage, name='homepage'),  # ✅ جعل الصفحة الرئيسية `/`
]
