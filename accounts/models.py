from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuid import uuid4  # ✅ توليد رمز تفعيل فريد


class CustomUser(AbstractUser):
    """
    ✅ المشرفون (`Superusers`) يتم تفعيلهم تلقائيًا عند إنشائهم (`is_active=True`).
    ✅ المستخدمون العاديون يحتاجون إلى موافقة لتفعيلهم (`is_active=False`).
    ✅ تسجيل دخول المشرفين يكون باسم المستخدم (`username`).
    ✅ تسجيل دخول المستخدمين العاديين يكون بالبريد الإلكتروني (`email`).
    ✅ لا يمكن للمستخدم العادي أن يكون مشرفًا (`superuser=False` افتراضيًا).
    ✅ إضافة رقم الجوال والسيرة الذاتية كمعلومات إضافية.
    ✅ إضافة رمز التفعيل (`activation_token`) لتفعيل الحساب عبر البريد الإلكتروني.
    """

    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")

    phone_number = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r"^05[0-9]{8}$", message="⚠️ رقم الجوال يجب أن يبدأ بـ 05 ويتكون من 10 أرقام.")]
    )

    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(['pdf'])],
        blank=True,
        null=True,
        verbose_name="السيرة الذاتية"
    )

    is_active = models.BooleanField(default=False, verbose_name="الحساب مفعل؟")

    activation_token = models.CharField(
        max_length=64,
        unique=True,
        blank=True,
        null=True,
        verbose_name="رمز التفعيل"
    )

    token_used = models.BooleanField(default=False, verbose_name="تم استخدام رمز التفعيل؟")

    USERNAME_FIELD = 'username'  # ✅ Django Admin يبقى كما هو
    REQUIRED_FIELDS = ['email']  # ✅ فقط البريد الإلكتروني مطلوب عند إنشاء المستخدمين العاديين

    def save(self, *args, **kwargs):
        """
        ✅ المشرفون (`Superusers`) يتم تفعيلهم تلقائيًا عند إنشائهم (`is_active=True`).
        ✅ المستخدمون العاديون يحتاجون إلى موافقة أو تفعيل عبر البريد (`is_active=False`).
        ✅ يتم إنشاء `activation_token` عند إنشاء الحساب لأول مرة فقط.
        ✅ بعد التفعيل، يتم تعيين `token_used=True` بدلاً من حذف `activation_token`.
        """

        if self.is_superuser:
            self.is_active = True  # ✅ المشرف يتم تفعيله تلقائيًا
        else:
            self.is_superuser = False
            self.is_staff = False  # ✅ التأكد من أن المستخدم العادي لا يكون موظفًا

        # ✅ إنشاء رمز التفعيل عند إنشاء الحساب لأول مرة فقط
        if not self.activation_token and not self.is_active:
            self.activation_token = str(uuid4())

        # ✅ عند التفعيل، يتم تعيين `token_used=True` لمنع إعادة استخدام التوكن
        if self.is_active and not self.token_used:
            self.token_used = True  

        super().save(*args, **kwargs)  # ✅ حفظ التغييرات في قاعدة البيانات

    def __str__(self):
        return self.username  # ✅ عرض اسم المستخدم بشكل صحيح


class AccountProfile(models.Model):
    """
    ✅ نموذج مخصص للمستخدمين العاديين فقط
    ✅ يتم إنشاؤه تلقائيًا عند إنشاء `CustomUser`
    ✅ يحتوي على نفس الحقول الخاصة بـ `CustomUser`
    ✅ تسجيل الدخول عبر البريد الإلكتروني وكلمة المرور
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="account_profile")

    email = models.EmailField(unique=True, verbose_name="البريد الإلكتروني")

    phone_number = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(regex=r"^05[0-9]{8}$", message="⚠️ رقم الجوال يجب أن يبدأ بـ 05 ويتكون من 10 أرقام.")]
    )

    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(['pdf'])],
        blank=True,
        null=True,
        verbose_name="السيرة الذاتية"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    def __str__(self):
        return f"حساب {self.user.username} ({self.email})"


# ✅ إنشاء `AccountProfile` تلقائيًا عند إنشاء مستخدم جديد
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        AccountProfile.objects.create(
            user=instance,
            email=instance.email,
            phone_number=instance.phone_number,
            resume=instance.resume
        )


# ✅ تحديث `AccountProfile` عند تحديث `CustomUser`
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'account_profile'):
        instance.account_profile.email = instance.email
        instance.account_profile.phone_number = instance.phone_number
        instance.account_profile.resume = instance.resume
        instance.account_profile.save()
