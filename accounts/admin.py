from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, AccountProfile

# ✅ إبقاء `CustomUserAdmin` كما هو في "المستخدمون" الافتراضي
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)

    fieldsets = (
        (_("معلومات الحساب"), {'fields': ('username', 'email', 'password')}),
        (_("معلومات شخصية"), {'fields': ('phone_number', 'resume')}),
        (_("الصلاحيات"), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_("تواريخ مهمة"), {'fields': ('last_login', 'date_joined')}),
    )

if not admin.site.is_registered(CustomUser):
    admin.site.register(CustomUser, CustomUserAdmin)

# ✅ تحسين `AccountProfileAdmin` ليتمكن من تفعيل وتعطيل الحسابات
class AccountProfileAdmin(admin.ModelAdmin):
    """
    🔹 يعرض المستخدمين العاديين فقط الذين ليسوا مشرفين.
    🔹 يتيح البحث والتصفية بناءً على البريد ورقم الجوال.
    🔹 يسمح بتفعيل أو تعطيل الحسابات مباشرة.
    """
    list_display = ('user', 'email', 'phone_number', 'is_active', 'created_at')
    search_fields = ('user__username', 'email', 'phone_number')
    ordering = ('created_at',)
    readonly_fields = ('created_at',)

    def is_active(self, obj):
        return obj.user.is_active
    is_active.boolean = True  # ✅ يجعلها تظهر كعلامة ✅ / ❌ في القائمة

    def activate_users(self, request, queryset):
        """ ✅ إجراء لتفعيل المستخدمين المحددين """
        count = 0
        for profile in queryset:
            profile.user.is_active = True  # ✅ تحديث `is_active` من `CustomUser`
            profile.user.save()
            count += 1

        self.message_user(request, _(f"✅ تم تفعيل {count} مستخدم بنجاح!"))  # 🔹 تم استخدام `gettext_lazy`

    def deactivate_users(self, request, queryset):
        """ ✅ إجراء لتعطيل المستخدمين المحددين """
        count = 0
        for profile in queryset:
            profile.user.is_active = False  # ✅ تحديث `is_active` من `CustomUser`
            profile.user.save()
            count += 1

        self.message_user(request, _(f"⚠️ تم تعطيل {count} مستخدم!"))  # 🔹 تم استخدام `gettext_lazy`

    activate_users.short_description = _("✅ تفعيل المستخدمين المحددين")
    deactivate_users.short_description = _("⚠️ تعطيل المستخدمين المحددين")

    actions = [activate_users, deactivate_users]  # ✅ إضافة الإجراءات إلى القائمة

    def get_queryset(self, request):
        """
        ✅ إظهار المستخدمين العاديين فقط في "الحسابات".
        """
        qs = super().get_queryset(request)
        return qs.filter(user__is_superuser=False)  # ✅ تصفية المشرفين بحيث لا يظهروا في قسم الحسابات

# ✅ تسجيل `AccountProfileAdmin` في لوحة تحكم Django
admin.site.register(AccountProfile, AccountProfileAdmin)
