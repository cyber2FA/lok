from django import forms  #  استيراد مكتبة النماذج (Forms) لإنشاء النموذج
from django.contrib.auth.forms import UserCreationForm  #  استيراد نموذج تسجيل المستخدم الافتراضي
from django.core.validators import FileExtensionValidator  #  استيراد المدقق لمنع رفع ملفات غير PDF
from .models import CustomUser  #  استيراد نموذج المستخدم المخصص لاستخدامه في التسجيل

class CustomUserCreationForm(UserCreationForm):
    """
    نموذج تسجيل مستخدم جديد مع التحقق من صحة البريد ورقم الجوال
    - يعتمد على `UserCreationForm` الافتراضي في Django، والذي يوفر إدارة تلقائية لكلمة المرور
    - يتحقق من أن البريد الإلكتروني ورقم الجوال غير مستخدمين مسبقًا
    - يسمح فقط بملفات PDF للسيرة الذاتية
    """

    email = forms.EmailField(required=True)  # 📌 حقل البريد الإلكتروني، مطلوب
    phone_number = forms.CharField(max_length=15, required=True)  # 📌 حقل رقم الجوال، مطلوب
    resume = forms.FileField(
        required=True, 
        validators=[FileExtensionValidator(['pdf'])]  # ✅ يمنع رفع أي ملفات غير PDF
    )

    class Meta:
        """
        يحدد الحقول المستخدمة في النموذج:
        - `username` (اسم المستخدم)
        - `email` (البريد الإلكتروني)
        - `phone_number` (رقم الجوال)
        - `password1` و `password2` (كلمة المرور وتأكيدها)
        - `resume` (السيرة الذاتية بصيغة PDF فقط)
        """
        model = CustomUser  # ✅ تحديد النموذج المرتبط به هذا الفورم
        fields = ['username', 'email', 'phone_number', 'password1', 'password2', 'resume']

    def clean_email(self):
        """
        التحقق من أن البريد الإلكتروني غير مسجل مسبقًا
        - يتم البحث في قاعدة البيانات عن البريد الإلكتروني، وإذا كان موجودًا، يتم إرجاع خطأ
        """
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("⚠️ البريد الإلكتروني مسجل بالفعل.")
        return email

    def clean_phone_number(self):
        """
        التحقق من أن رقم الجوال غير مسجل مسبقًا
        - يتم البحث في قاعدة البيانات عن رقم الجوال، وإذا كان موجودًا، يتم إرجاع خطأ
        """
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("⚠️ رقم الجوال مسجل بالفعل.")
        return phone_number
