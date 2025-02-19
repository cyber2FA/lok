from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    تخصيص عرض المستخدمين في لوحة التحكم:
    - عرض الحقول الإضافية مثل رقم الجوال والسيرة الذاتية
    - ترتيب الحقول في لوحة التحكم
    """
    fieldsets = UserAdmin.fieldsets + (
        ('معلومات إضافية', {'fields': ('phone_number', 'resume')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('معلومات إضافية', {'fields': ('phone_number', 'resume')}),
    )
    list_display = ('username', 'email', 'phone_number', 'is_staff', 'is_active')  # 📌 عرض هذه الحقول في قائمة المستخدمين

admin.site.register(CustomUser, CustomUserAdmin)  # 📌 تسجيل النموذج في لوحة التحكم
