"""
إعدادات Django لمشروع lockauth.

تم إنشاؤه باستخدام 'django-admin startproject' مع Django 5.1.1.

لمزيد من المعلومات حول هذا الملف، راجع:
https://docs.djangoproject.com/en/5.1/topics/settings/
"""

from pathlib import Path
import os
import dj_database_url  # مكتبة لتحليل وإدارة اتصال قاعدة البيانات عبر `DATABASE_URL`
from dotenv import load_dotenv  # تحميل متغيرات البيئة من `.env`

# 🔹 تحميل متغيرات البيئة من ملف `.env`
load_dotenv()

# 🔹 تحديد المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# 🚨 مفتاح الأمان (يتم تخزينه في `.env` لحماية المشروع)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-default-secret-key')

# ⚠️ وضع التصحيح (يجب أن يكون `False` في الإنتاج)
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# 🖥️ النطاقات المسموح لها بالوصول إلى السيرفر (يتم تحميلها من `.env`)
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# 🔹 التطبيقات المثبتة في المشروع
INSTALLED_APPS = [
    'django.contrib.admin',  # لوحة تحكم المشرف
    'django.contrib.auth',  # نظام المصادقة
    'django.contrib.contenttypes',  # إدارة الأنواع والمحتويات
    'django.contrib.sessions',  # إدارة الجلسات
    'django.contrib.messages',  # إدارة الرسائل والتنبيهات
    'django.contrib.staticfiles',  # إدارة الملفات الثابتة (CSS, JavaScript, Images)

    # ✅ إضافة تطبيق إدارة المستخدمين
    'accounts',
]

# 🔹 الوسائط (Middleware) المستخدمة في المشروع
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # تحسين الأمان والحماية من الهجمات
    'django.contrib.sessions.middleware.SessionMiddleware',  # إدارة الجلسات
    'django.middleware.common.CommonMiddleware',  # دعم الطلبات العامة وتحسين الأداء
    'django.middleware.csrf.CsrfViewMiddleware',  # حماية CSRF لمنع الهجمات عبر النماذج
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # إدارة المصادقة
    'django.contrib.messages.middleware.MessageMiddleware',  # دعم الرسائل والتنبيهات
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # الحماية من Clickjacking
    'accounts.middleware.AutoLogoutMiddleware',  # تسجيل الخروج التلقائي عند الخمول
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

# 🔹 تحديد نوع البيئة (الإفتراضي: `development`)
ENVIRONMENT = os.getenv('DJANGO_ENV', 'development')

# 🔹 إعدادات قاعدة البيانات (SQLite للتطوير - PostgreSQL للإنتاج)
if ENVIRONMENT == 'production':
    DATABASES = {
        'default': dj_database_url.config(  # استخدام `dj_database_url` لتحليل `DATABASE_URL`
            default=os.getenv('DATABASE_URL')
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# 🔹 إعدادات التحقق من كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 دعم اللغات (العربية والإنجليزية)
LANGUAGES = [
    ('ar', 'Arabic'),  # 🌍 اللغة العربية
    ('en', 'English'),  # 🌍 اللغة الإنجليزية
]

# 🔹 تحديد اللغة الافتراضية (العربية)
LANGUAGE_CODE = 'ar'

# ⏰ إعدادات المنطقة الزمنية (حسب منطقتك)
TIME_ZONE = 'Asia/Riyadh'

USE_I18N = True  # تمكين الترجمة الدولية
USE_L10N = True  # تمكين تنسيق الأرقام والتواريخ حسب اللغة
USE_TZ = True  # استخدام التوقيت الزمني الموحد

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

# 🔹 إعدادات البريد الإلكتروني باستخدام Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # البريد الافتراضي للمرسل

# ✅ مدة الجلسة تنتهي بعد 5 دقائق من عدم النشاط
SESSION_COOKIE_AGE = 300  # بالثواني (5 دقائق = 300 ثانية)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # إنهاء الجلسة عند إغلاق المتصفح
SESSION_SAVE_EVERY_REQUEST = True  # تحديث مهلة الجلسة عند كل طلب جديد
