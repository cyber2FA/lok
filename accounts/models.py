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

    USERNAME_FIELD = 'username'  # ✅ Django Admin يبقى كما هو
    REQUIRED_FIELDS = ['email']  # ✅ فقط البريد الإلكتروني مطلوب عند إنشاء المستخدمين العاديين

    def save(self, *args, **kwargs):
        """
        ✅ جعل المشرفين مفعلين تلقائيًا عند إنشائهم، بينما المستخدم العادي يحتاج إلى موافقة أو تفعيل عبر البريد.
        ✅ يتم إنشاء رمز تفعيل عشوائي عند إنشاء الحساب لأول مرة.
        """
        if self.is_superuser:
            self.is_active = True  # ✅ المشرف يتم تفعيله تلقائيًا
        else:
            self.is_superuser = False
            self.is_staff = False  # ✅ التأكد من أن المستخدم العادي لا يكون موظفًا

        # ✅ إنشاء رمز تفعيل إذا لم يكن موجودًا والمستخدم غير مفعل
        if not self.activation_token and not self.is_active:
            self.activation_token = str(uuid4())

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username  # ✅ Django Admin يعرض اسم المستخدم كما هو افتراضيًا


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
