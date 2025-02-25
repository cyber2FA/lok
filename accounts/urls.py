from django.urls import path
from .views import (
    register, homepage, dashboard, pending_activation, update_profile, activate_account,  
    validate_username, validate_email, validate_phone_number,
    CustomLoginView, redirect_after_login  # ✅ استيراد الفيوهات المطلوبة
)
from .views import logout_view  # ✅ استيراد فيو تسجيل الخروج المخصص

urlpatterns = [
    # ✅ 🌍 المسارات الأساسية
    path('', homepage, name='homepage'),  # الصفحة الرئيسية
    path('dashboard/', dashboard, name='dashboard'),  # ✅ توجيه المستخدم العادي إلى `dashboard.html`
    path('register/', register, name='register'),  # صفحة إنشاء الحساب
    path('login/', CustomLoginView.as_view(), name='login'),  # ✅ تسجيل الدخول المخصص
    path('pending-activation/', pending_activation, name='pending_activation'),  # صفحة انتظار التفعيل
    path('update-profile/', update_profile, name='update_profile'),  # ✅ تعديل بيانات الحساب

    # ✅ 📩 تفعيل الحساب عبر البريد الإلكتروني
    path('verify-account/<str:token>/', activate_account, name='activate_account'),

    # ✅ 🔍 مسارات التحقق الفوري عبر `AJAX`
    path('validate-username/', validate_username, name='validate_username'),
    path('validate-email/', validate_email, name='validate_email'),
    path('validate-phone-number/', validate_phone_number, name='validate_phone_number'),

    # ✅ 🔀 التوجيه بعد تسجيل الدخول بناءً على نوع المستخدم
    path('redirect/', redirect_after_login, name='redirect_after_login'),  
    path('profile/', update_profile, name='profile'),  # ✅ إضافة مسار إعدادات الحساب
    path('logout/', logout_view, name='logout'),


]
