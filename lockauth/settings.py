"""
إعدادات Django لمشروع lockauth.

تم إنشاؤه باستخدام 'django-admin startproject' مع Django 5.1.1.

لمزيد من المعلومات حول هذا الملف، راجع:
https://docs.djangoproject.com/en/5.1/topics/settings/
"""

from pathlib import Path
import os

# 🔹 تحديد المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# 🚨 مفتاح الأمان (يُفضل تخزينه في .env وعدم وضعه مباشرة هنا في الإنتاج)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-ewblh2nb9s6-v612qs-fzt0a38m*8lmwpt7=dm$@+^s0_91n@_')

# ⚠️ تفعيل وضع التطوير (يجب أن يكون False في الإنتاج)
DEBUG = True

# 🖥️ تحديد النطاقات المسموح لها بالوصول إلى السيرفر (قم بإضافة نطاقات الإنتاج هنا)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'lockauth.onrender.com']


# 🔹 التطبيقات المثبتة في المشروع
INSTALLED_APPS = [
    'django.contrib.admin',            # لوحة تحكم المشرف
    'django.contrib.auth',             # نظام المصادقة والتحكم بالمستخدمين
    'django.contrib.contenttypes',     # إدارة الأنواع والمحتويات
    'django.contrib.sessions',         # إدارة الجلسات (Sessions)
    'django.contrib.messages',         # نظام الرسائل والتنبيهات
    'django.contrib.staticfiles',      # إدارة الملفات الثابتة (CSS, JavaScript, Images)

    # ✅ إضافة تطبيق إدارة المستخدمين
    'accounts',
]

# 🔹 الوسائط (Middleware) المستخدمة في المشروع
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # تحسين الأمان
    'django.contrib.sessions.middleware.SessionMiddleware',   # إدارة الجلسات
    'django.middleware.common.CommonMiddleware',              # دعم الطلبات العامة
    'django.middleware.csrf.CsrfViewMiddleware',             # حماية CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',# إدارة المصادقة
    'django.contrib.messages.middleware.MessageMiddleware',   # دعم الرسائل
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # الحماية من Clickjacking
]

# 🔹 ضبط ملف URL الرئيسي للمشروع
ROOT_URLCONF = 'lockauth.urls'

# 🔹 إعدادات القوالب (Templates)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # 📌 إضافة مجلد القوالب الرئيسي
        'APP_DIRS': True,  # السماح باستخدام القوالب داخل التطبيقات
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 🔹 تحديد تطبيق WSGI الخاص بالمشروع
WSGI_APPLICATION = 'lockauth.wsgi.application'


# 🔹 إعدادات قاعدة البيانات (قاعدة بيانات SQLite الافتراضية)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# 🔹 إعدادات التحقق من كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 🌍 دعم اللغات (العربية والإنجليزية)
LANGUAGES = [
    ('ar', 'Arabic'),  # 🌍 اللغة العربية
    ('en', 'English'), # 🌍 اللغة الإنجليزية
]

# 🔹 تحديد اللغة الافتراضية (العربية)
LANGUAGE_CODE = 'ar'

# ⏰ إعدادات المنطقة الزمنية (قم بتغييرها حسب موقعك)
TIME_ZONE = 'Asia/Riyadh'

USE_I18N = True  # تمكين الترجمة الدولية
USE_L10N = True  # تمكين تنسيق الأرقام والتواريخ حسب اللغة
USE_TZ = True    # استخدام التوقيت الزمني الموحد


# 📁 إعدادات الملفات الثابتة (Static Files مثل CSS و JavaScript)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]  # مجلد إضافي للملفات الثابتة

# 📁 إعدادات ملفات الوسائط (Media مثل صور المستخدمين)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # المسار الذي يتم حفظ الملفات فيه


# ✅ تحديد نموذج المستخدم المخصص
AUTH_USER_MODEL = 'accounts.CustomUser'

# 🔹 تحديد المفتاح الافتراضي عند إنشاء الجداول
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#  إعدادات إرسال البريد الإلكتروني باستخدام Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'SecureAuthSys@gmail.com'  #  بريد Gmail
EMAIL_HOST_PASSWORD = 'wxlg ckfp kknp lezc'  #  كلمة مرور التطبيق (وليس كلمة مرور الحساب العادية)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  #  البريد الافتراضي للمرسل
