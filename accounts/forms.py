from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator, RegexValidator
from .models import CustomUser, AccountProfile

class CustomUserCreationForm(UserCreationForm):
    """
    ✅ نموذج تسجيل مستخدم جديد مع التحقق الفوري من الأخطاء عبر `AJAX`
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@email.com',
            'data-validation': 'email',
            'data-url': '/validate-email/'
        }),
        error_messages={'unique': "⚠️ البريد الإلكتروني مسجل بالفعل، يرجى استخدام بريد آخر."}
    )

    phone_number = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '05xxxxxxxx',
            'data-validation': 'phone',
            'data-url': '/validate-phone-number/'
        }),
        validators=[
            RegexValidator(
                regex=r"^05[0-9]{8}$",
                message="⚠️ رقم الجوال يجب أن يتكون من 10 أرقام فقط ويبدأ بـ 05."
            )
        ],
        error_messages={'unique': "⚠️ رقم الجوال مسجل بالفعل، يرجى استخدام رقم آخر."}
    )

    resume = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'data-validation': 'resume'
        }),
        validators=[FileExtensionValidator(['pdf'])],
        error_messages={'invalid_extension': "⚠️ يُسمح فقط بملفات PDF!"}
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2', 'resume']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'اسم المستخدم',
                'data-validation': 'username',
                'data-url': '/validate-username/'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '********',
                'data-validation': 'password1'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '********',
                'data-validation': 'password2'
            }),
        }

    def clean(self):
        """
        ✅ التحقق من جميع الحقول مرة واحدة قبل الحفظ النهائي
        """
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')
        resume = cleaned_data.get('resume')

        errors = {}

        # ✅ التحقق من اسم المستخدم
        if username and CustomUser.objects.filter(username=username).exists():
            errors['username'] = "⚠️ اسم المستخدم مسجل بالفعل، يرجى اختيار اسم آخر."

        # ✅ التحقق من البريد الإلكتروني
        if email and (CustomUser.objects.filter(email=email).exists() or AccountProfile.objects.filter(email=email).exists()):
            errors['email'] = "⚠️ البريد الإلكتروني مسجل بالفعل، يرجى استخدام بريد آخر."

        # ✅ التحقق من رقم الجوال
        if phone_number and (CustomUser.objects.filter(phone_number=phone_number).exists() or AccountProfile.objects.filter(phone_number=phone_number).exists()):
            errors['phone_number'] = "⚠️ رقم الجوال مسجل بالفعل، يرجى استخدام رقم آخر."

        # ✅ التحقق من حجم السيرة الذاتية
        if resume and resume.size > 2 * 1024 * 1024:  # 2MB
            errors['resume'] = "⚠️ حجم الملف يجب أن يكون أقل من 2MB!"

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data


class AccountProfileForm(forms.ModelForm):
    """
    ✅ نموذج تحديث ملف الحساب الشخصي
    """

    class Meta:
        model = AccountProfile
        fields = ['email', 'phone_number', 'resume']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@email.com'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '05xxxxxxxx'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
