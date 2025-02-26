from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve  # view لتقديم الملفات الثابتة
from accounts.views import homepage  # استيراد الصفحة الرئيسية

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', homepage, name='homepage'),
]

# في وضع التطوير، يمكن استخدام دالة static() لتقديم الملفات الإعلامية والثابتة
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # نفترض أن ملفاتك الثابتة موجودة في المجلد الأول من STATICFILES_DIRS (مثلاً: BASE_DIR / "static")
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
else:
    # في بيئة الإنتاج، نجبر Django على تقديم الملفات باستخدام view serve
    urlpatterns += [
        # تقديم الملفات الإعلامية (Media)
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        # تقديم الملفات الثابتة (Static) من مجلدك المستخدم أثناء التطوير
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS[0]}),
    ]
