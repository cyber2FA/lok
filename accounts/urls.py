from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    # ✅ الفيوهات الأساسية
    register, homepage, dashboard, pending_activation, update_profile, activate_account,  # ✅ تعديل `verify_account` ليكون `activate_account`
    
    # ✅ الفيوهات الخاصة بالتحقق الفوري عبر `AJAX`
    validate_username, validate_email, validate_phone_number,
    
    # ✅ تخصيص تسجيل الدخول
    CustomLoginView
)

urlpatterns = [
    # ✅ 🌍 المسارات الأساسية
    path('', homepage, name='homepage'),  # الصفحة الرئيسية
    path('dashboard/', dashboard, name='dashboard'),  # لوحة التحكم بعد تسجيل الدخول
    path('register/', register, name='register'),  # صفحة إنشاء الحساب
    path('login/', CustomLoginView.as_view(), name='login'),  # ✅ تسجيل الدخول المخصص
    path('logout/', LogoutView.as_view(next_page='homepage'), name='logout'),  # ✅ تسجيل الخروج
    path('pending-activation/', pending_activation, name='pending_activation'),  # صفحة انتظار التفعيل
    path('update-profile/', update_profile, name='update_profile'),  # ✅ تعديل بيانات الحساب

    # ✅ 📩 تفعيل الحساب عبر البريد الإلكتروني
    path('verify-account/<str:token>/', activate_account, name='activate_account'),  # ✅ رابط التفعيل الصحيح

    # ✅ 🔍 مسارات التحقق الفوري عبر `AJAX`
    path('validate-username/', validate_username, name='validate_username'),  # التحقق من توفر اسم المستخدم
    path('validate-email/', validate_email, name='validate_email'),  # التحقق من توفر البريد الإلكتروني
    path('validate-phone-number/', validate_phone_number, name='validate_phone_number'),  # التحقق من توفر رقم الجوال
]
