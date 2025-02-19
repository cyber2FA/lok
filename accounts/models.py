from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator

class CustomUser(AbstractUser):
    """
    نموذج مستخدم مخصص يمتد من AbstractUser ويضيف حقولًا جديدة:
    - البريد الإلكتروني (فريد)
    - رقم الجوال (فريد)
    - ملف السيرة الذاتية (PDF فقط)
    """
    email = models.EmailField(unique=True)  #  تأكيد أن البريد الإلكتروني فريد
    phone_number = models.CharField(max_length=15, unique=True)  #  تأكيد أن رقم الجوال فريد
    resume = models.FileField(upload_to='resumes/', validators=[FileExtensionValidator(['pdf'])])  #  يقبل ملفات PDF فقط

    def __str__(self):
        return self.username  #  إرجاع اسم المستخدم عند الطباعة أو العرض
