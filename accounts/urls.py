from django.urls import path
from .views import register, homepage, dashboard  # استيراد جميع الفيوهات المطلوبة
from django.contrib.auth.views import LoginView  # استيراد فيو تسجيل الدخول  الجاهز من Django

urlpatterns = [
    path('', homepage, name='homepage'),  # الصفحة الرئيسية
    path('dashboard/', dashboard, name='dashboard'),  # لوحة التحكم بعد تسجيل الدخول التي تظهر للعميل 
    path('register/', register, name='register'),  # صفحة إنشاء الحساب
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # صفحة تسجيل الدخول
]
