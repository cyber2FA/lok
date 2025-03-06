from django.urls import path
from .views import (
    register, homepage, dashboard, pending_activation, update_profile, activate_account,  
    validate_username, validate_email, validate_phone_number,
    CustomLoginView, redirect_after_login, logout_view,
    password_reset_request, password_reset_confirm, password_reset_invalid
)

urlpatterns = [
    # ✅ 🌍 المسارات الأساسية
    path('', homepage, name='homepage'),  # الصفحة الرئيسية
    path('dashboard/', dashboard, name='dashboard'),  # ✅ توجيه المستخدم العادي إلى `dashboard.html`
    path('register/', register, name='register'),  # صفحة إنشاء الحساب
    path('login/', CustomLoginView.as_view(), name='login'),  # ✅ تسجيل الدخول المخصص
    path('pending-activation/', pending_activation, name='pending_activation'),  # صفحة انتظار التفعيل
    path('update-profile/', update_profile, name='update_profile'),  # ✅ تعديل بيانات الحساب

    # ✅ 📩 تفعيل الحساب عبر البريد الإلكتروني
    path('verify-account/<str:token>/', activate_account, name='activate_account'),  # ✅ التأكد من التوجيه الصحيح

    # ✅ 🔍 مسارات التحقق الفوري عبر `AJAX`
    path('validate-username/', validate_username, name='validate_username'),
    path('validate-email/', validate_email, name='validate_email'),
    path('validate-phone-number/', validate_phone_number, name='validate_phone_number'),

    # ✅ 🔀 التوجيه بعد تسجيل الدخول بناءً على نوع المستخدم
    path('redirect/', redirect_after_login, name='redirect_after_login'),  
    path('profile/', update_profile, name='profile'),  # ✅ إعدادات الحساب
    path('logout/', logout_view, name='logout'),  # ✅ تسجيل الخروج

    # ✅ 🔐 استعادة كلمة المرور
    path("password-reset/", password_reset_request, name="password_reset"),
    path("password-reset-confirm/<uidb64>/<token>/", password_reset_confirm, name="password_reset_confirm"),
    path("password-reset-invalid/", password_reset_invalid, name="password_reset_invalid"),
]
