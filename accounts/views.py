from django.shortcuts import render, redirect  # استيراد دوال عرض القوالب وإعادة التوجيه
from django.contrib import messages  # استيراد نظام الرسائل في Django لإرسال إشعارات للمستخدم
from django.http import JsonResponse, HttpResponseRedirect  # استيراد `JsonResponse` للاستجابات JSON و `HttpResponseRedirect` لإعادة التوجيه
from django.db import IntegrityError  # استيراد استثناء `IntegrityError` للتعامل مع أخطاء قاعدة البيانات
from django.contrib.auth.decorators import login_required  # استيراد `login_required` لتقييد الوصول إلى بعض الصفحات للمستخدمين المسجلين فقط
from django.contrib.auth.views import LoginView  # استيراد `LoginView` لاستخدام نظام تسجيل الدخول المدمج في Django
from .forms import CustomUserCreationForm, AccountProfileForm  # استيراد نماذج إنشاء المستخدم وتحديث الحساب الشخصي
from .models import CustomUser, AccountProfile  # استيراد نماذج المستخدم (`CustomUser`) والملف الشخصي (`AccountProfile`)
import logging  # استيراد `logging` لتسجيل الأخطاء والمعلومات أثناء تشغيل التطبيق
from django.urls import reverse  # استيراد `reverse` لإنشاء روابط ديناميكية للمسارات في Django
from django.core.mail import send_mail  # استيراد `send_mail` لإرسال البريد الإلكتروني عبر Django
import uuid  # استيراد `uuid` لإنشاء رموز فريدة تستخدم في تأكيد الحسابات


# إعداد سجل الأخطاء
logger = logging.getLogger(__name__)

### ✅ **🔹 الفيوهات الرئيسية**
def homepage(request):
    return render(request, 'homepage.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def pending_activation(request):
    return render(request, 'pending_activation.html')

### ✅ **🔹 فيو تسجيل الدخول المخصص**
class CustomLoginView(LoginView):
    template_name = 'login.html'  


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)

        # ✅ دعم AJAX للتحقق الفوري من المدخلات
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if form.is_valid():
                return JsonResponse({'valid': True})
            else:
                errors = {field: [error for error in error_list] for field, error_list in form.errors.items()}
                return JsonResponse({'valid': False, 'errors': errors}, status=400)

        # ✅ عند تقديم النموذج بشكل عادي وليس عبر `AJAX`
        if form.is_valid():
            try:
                email = form.cleaned_data.get('email')
                phone_number = form.cleaned_data.get('phone_number')

                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "⚠️ البريد الإلكتروني مستخدم بالفعل، يرجى استخدام بريد آخر.")
                    return render(request, 'register.html', {'form': form})

                if CustomUser.objects.filter(phone_number=phone_number).exists():
                    messages.error(request, "⚠️ رقم الجوال مستخدم بالفعل، يرجى استخدام رقم آخر.")
                    return render(request, 'register.html', {'form': form})

                # ✅ حفظ المستخدم فقط إذا لم يكن موجودًا بالفعل
                user = form.save(commit=False)
                user.is_active = False  # ✅ الحساب يبقى غير مفعل حتى موافقة المشرف
                user.activation_token = str(uuid.uuid4())  # ✅ إنشاء رمز التفعيل
                user.save()

                # ✅ التحقق مما إذا كان `AccountProfile` موجودًا مسبقًا لتجنب الخطأ
                profile, created = AccountProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'email': user.email,
                        'phone_number': user.phone_number,
                        'resume': user.resume
                    }
                )

                if not created:
                    logger.warning(f"⚠️ AccountProfile موجود مسبقًا للمستخدم {user.email}, لم يتم إنشاؤه مجددًا.")

                # ✅ إرسال بريد التفعيل
                activation_link = request.build_absolute_uri(
                    reverse('activate_account', kwargs={'token': user.activation_token})
                )
                send_mail(
                    'تأكيد حسابك في منصتنا 🎉',
                    f'مرحبًا {user.username}،\n\nاضغط على الرابط التالي لتفعيل حسابك:\n{activation_link}',
                    'SecureAuthSys@gmail.com',
                    [user.email],
                    fail_silently=False,
                )

                request.session.flush()  # ✅ حذف الجلسات السابقة بعد التسجيل
                
                messages.success(request, "✅ تم تسجيل حسابك بنجاح! تحقق من بريدك الإلكتروني لتفعيل الحساب.")
                return HttpResponseRedirect(reverse('pending_activation'))  

            except IntegrityError as e:
                logger.error(f"❌ خطأ في قاعدة البيانات أثناء التسجيل: {e}")
                messages.error(request, "⚠️ حدث خطأ أثناء التسجيل، يرجى المحاولة لاحقًا.")
                return redirect('register')

            except Exception as e:
                logger.error(f"❌ خطأ غير متوقع أثناء التسجيل: {e}")
                messages.error(request, "⚠️ حدث خطأ غير متوقع، يرجى المحاولة لاحقًا.")
                return redirect('register')

        else:
            messages.error(request, "⚠️ يوجد أخطاء في النموذج، يرجى تصحيحها قبل المتابعة.")

    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def activate_account(request, token):
    try:
        user = CustomUser.objects.get(activation_token=token, is_active=False)
        user.is_active = True  # ✅ تفعيل الحساب
        user.activation_token = None  # ✅ مسح رمز التفعيل بعد الاستخدام
        user.save()

        messages.success(request, "✅ تم تفعيل حسابك بنجاح! يمكنك الآن تسجيل الدخول.")
        return render(request, 'account_verified.html')

    except CustomUser.DoesNotExist:
        messages.error(request, "⚠️ رابط التفعيل غير صالح أو الحساب مفعّل مسبقًا.")
        return render(request, 'account_verification_failed.html')

### ✅ **🔹 فيو تحديث الحساب الشخصي**
@login_required
def update_profile(request):
    try:
        profile = request.user.account_profile  

        if request.method == 'POST':
            form = AccountProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "✅ تم تحديث حسابك بنجاح!")
                return redirect('dashboard')
            else:
                messages.error(request, "⚠️ يوجد أخطاء في البيانات المدخلة.")
        else:
            form = AccountProfileForm(instance=profile)

        return render(request, 'update_profile.html', {'form': form})

    except AccountProfile.DoesNotExist:
        messages.error(request, "⚠️ لم يتم العثور على الملف الشخصي!")
        return redirect('dashboard')

### ✅ **🔹 فيوز التحقق الفوري من الحقول الفريدة**
def validate_username(request):
    username = request.GET.get("value", "").strip()
    if CustomUser.objects.filter(username=username).exists():
        return JsonResponse({"exists": True, "message": "❌ اسم المستخدم مسجل بالفعل!"})
    return JsonResponse({"exists": False, "message": "✅ اسم المستخدم متاح!"})

def validate_email(request):
    email = request.GET.get("value", "").strip()
    if CustomUser.objects.filter(email=email).exists() or AccountProfile.objects.filter(email=email).exists():
        return JsonResponse({"exists": True, "message": "❌ البريد الإلكتروني مستخدم بالفعل!"})
    return JsonResponse({"exists": False, "message": "✅ البريد الإلكتروني متاح!"})

def validate_phone_number(request):
    phone_number = request.GET.get("value", "").strip()
    if CustomUser.objects.filter(phone_number=phone_number).exists() or AccountProfile.objects.filter(phone_number=phone_number).exists():
        return JsonResponse({"exists": True, "message": "❌ رقم الجوال مستخدم بالفعل!"})
    return JsonResponse({"exists": False, "message": "✅ رقم الجوال متاح!"})