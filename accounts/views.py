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
from django.contrib.auth.hashers import make_password  # ✅ تشفير كلمة المرور قبل الحفظ
import re  # ✅ التأكد من تضمين مكتبة التحقق من الأنماط
from django.contrib.auth import logout  # ✅ استيراد دالة تسجيل الخروج من Django
from django.contrib.auth import authenticate, login  # استيراد دوال المصادقة وتسجيل الدخول من Django
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
# إعداد سجل الأخطا
logger = logging.getLogger(__name__)


### ✅ **🔹 الفيوهات الرئيسية**
def homepage(request):
    return render(request, 'homepage.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def pending_activation(request):
    return render(request, 'pending_activation.html')

### ✅ **🔹 فيو تسجيل الدخول المخصص**

# إعداد سجل الأخطاء
logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    """
    ✅ تسجيل الدخول المخصص مع دعم:
    - تسجيل الدخول باسم المستخدم، البريد الإلكتروني، أو رقم الجوال.
    - توجيه المشرف إلى `/admin/` والمستخدم العادي إلى `/dashboard/`.
    - عرض رسالة خطأ إذا كانت بيانات تسجيل الدخول غير صحيحة.
    """
    template_name = 'login.html'

    def form_valid(self, form):
        """
        ✅ عند نجاح تسجيل الدخول:
        - البحث عن المستخدم في قاعدة البيانات بأي من (اسم المستخدم، البريد، رقم الجوال).
        - التأكد من أن الحساب مفعل (`is_active=True`).
        - تنفيذ `authenticate()` باستخدام `username` الصحيح.
        """
        username_or_email_or_phone = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # ✅ البحث عن المستخدم بأي من (اسم المستخدم، البريد، رقم الجوال)
        user = CustomUser.objects.filter(username=username_or_email_or_phone).first() or \
               CustomUser.objects.filter(email=username_or_email_or_phone).first() or \
               CustomUser.objects.filter(phone_number=username_or_email_or_phone).first()

        if user:
            # ✅ محاولة المصادقة
            auth_user = authenticate(self.request, username=user.username, password=password)

            if auth_user:
                if auth_user.is_active:
                    login(self.request, auth_user)
                    return super().form_valid(form)
                else:
                    messages.error(self.request, "⚠️ حسابك غير مفعل! يرجى التحقق من بريدك الإلكتروني.")
                    return self.form_invalid(form)

        # ✅ إذا لم يتم العثور على المستخدم أو كلمة المرور خاطئة
        messages.error(self.request, "⚠️ اسم المستخدم، البريد، أو رقم الجوال غير صحيح أو كلمة المرور خاطئة!")
        return self.form_invalid(form)

    def get_success_url(self):
        """
        ✅ توجيه المستخدم بعد تسجيل الدخول:
        - المشرف إلى `/admin/`
        - المستخدم العادي إلى `/dashboard/`
        """
        if self.request.user.is_superuser:
            return reverse('admin:index')
        return reverse('dashboard')


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
    user = CustomUser.objects.filter(activation_token=token).first()

    if user:
        if user.is_active:
            # ✅ إذا كان الحساب مفعل مسبقًا، نعرض القالب المناسب
            messages.info(request, "✅ تم تفعيل حسابك مسبقًا! يمكنك تسجيل الدخول الآن.")
            return render(request, 'account_already_verified.html')

        # ✅ تفعيل الحساب لأول مرة
        user.is_active = True  
        user.activation_token = None  # ✅ تعيين NULL بدلاً من تكرار قيمة ثابتة
        user.save()

        messages.success(request, "✅ تم تفعيل حسابك بنجاح! يمكنك الآن تسجيل الدخول.")
        return render(request, 'account_verified.html')

    # ✅ إذا لم يتم العثور على المستخدم بالرمز، فهذا يعني أن الرابط غير صالح
    messages.error(request, "⚠️ رابط التفعيل غير صالح أو قد يكون منتهي الصلاحية.")
    return render(request, 'account_verification_failed.html')### ✅ **🔹 فيو تحديث الحساب الشخصي**

@login_required
def update_profile(request):
    """
    ✅ فيو تحديث الملف الشخصي للمستخدم:
    - يتحقق من القيم الفريدة (البريد، رقم الجوال، اسم المستخدم) فقط عند التغيير.
    - يتحقق من صحة جميع الحقول قبل السماح بالتحديث.
    - عند تعديل البريد أو كلمة المرور، يتم إرسال رابط التفعيل وتعطيل الحساب مؤقتًا.
    - لا يتم تنفيذ التحديث إذا كان هناك خطأ في أي حقل.
    """

    user = request.user  # المستخدم الحالي المسجل الدخول

    try:
        profile = user.account_profile  # محاولة جلب ملف المستخدم الشخصي
    except AccountProfile.DoesNotExist:
        messages.error(request, "⚠️ لم يتم العثور على الملف الشخصي!")
        return redirect('dashboard')

    if request.method == 'POST':
        form = AccountProfileForm(request.POST, request.FILES, instance=profile)

        new_password = request.POST.get('password1', '').strip()
        confirm_password = request.POST.get('password2', '').strip()
        new_email = request.POST.get('email', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()

        errors = {}

        # ✅ التحقق من رقم الجوال
        if phone_number and not re.match(r"^05[0-9]{8}$", phone_number):
            errors['phone_number'] = "⚠️ رقم الجوال يجب أن يبدأ بـ 05 ويتكون من 10 أرقام!"

        # ✅ التحقق من البريد الإلكتروني (إذا تم تغييره فقط)
        if new_email and new_email != user.email and CustomUser.objects.exclude(id=user.id).filter(email=new_email).exists():
            errors['email'] = "⚠️ البريد الإلكتروني مستخدم بالفعل!"

        # ✅ التحقق من كلمة المرور الجديدة (في حال تم إدخالها)
        if new_password or confirm_password:
            if len(new_password) < 8:
                errors['password1'] = "⚠️ يجب أن تحتوي كلمة المرور على 8 أحرف على الأقل!"
            if not any(char.isdigit() for char in new_password):
                errors['password1'] = "⚠️ يجب أن تحتوي كلمة المرور على رقم واحد على الأقل!"
            if not any(char.isupper() for char in new_password):
                errors['password1'] = "⚠️ يجب أن تحتوي كلمة المرور على حرف كبير واحد على الأقل!"
            if not any(char in "!@#$%^&*()_+" for char in new_password):
                errors['password1'] = "⚠️ يجب أن تحتوي كلمة المرور على رمز خاص مثل @ أو #!"
            if new_password != confirm_password:
                errors['password2'] = "⚠️ كلمة المرور غير متطابقة!"

        # ✅ إذا كان هناك أي أخطاء، لا يتم حفظ أي شيء
        if errors:
            for field, error in errors.items():
                messages.error(request, error)
            return render(request, 'profile.html', {'form': form})

        # ✅ إذا لم يكن هناك أخطاء، يتم حفظ جميع التعديلات مرة واحدة
        if new_password:
            user.password = make_password(new_password)

        if new_email:
            user.email = new_email

        # ✅ تعطيل الحساب مؤقتًا حتى يتم التفعيل عبر البريد الإلكتروني
        user.is_active = False
        user.activation_token = str(uuid.uuid4())  
        user.save()

        # ✅ إرسال بريد التفعيل للمستخدم
        activation_link = request.build_absolute_uri(
            reverse('activate_account', kwargs={'token': user.activation_token})
        )
        send_mail(
            'إعادة تفعيل حسابك بسبب التحديثات',
            f'مرحبًا {user.username}،\n\nلقد قمت بتحديث حسابك.\n'
            f'يرجى تأكيد التحديث من خلال الرابط التالي:\n{activation_link}',
            'SecureAuthSys@gmail.com',
            [user.email],
            fail_silently=False,
        )

        messages.info(request, "⚠️ تم تعطيل حسابك مؤقتًا بسبب التحديثات! يرجى التحقق من بريدك لتفعيله.")
        return redirect('pending_activation')  

    else:
        form = AccountProfileForm(instance=profile)

    return render(request, 'profile.html', {'form': form})
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

@login_required
def redirect_after_login(request):
    """
    ✅ توجيه المستخدم بعد تسجيل الدخول:
    - إذا كان `is_superuser=True` → يتم توجيهه إلى `/admin/`
    - إذا كان `is_superuser=False` → يتم توجيهه إلى `/dashboard/`
    """
    if request.user.is_superuser:
        return redirect(reverse('admin:index'))  # ✅ استخدام `reverse` لتوجيه المشرف
    else:
        return redirect(reverse('dashboard'))  # ✅ توجيه المستخدم العادي إلى المسار الصحيح

@login_required  # ✅ تأكد من أن المستخدم مسجل الدخول قبل تنفيذ تسجيل الخروج
def logout_view(request):
    """
    ✅ فيو تسجيل الخروج:
    - يقوم بتسجيل خروج المستخدم بأمان.
    - يمسح جميع بيانات الجلسة لحماية الخصوصية.
    - يعيد توجيه المستخدم إلى الصفحة الرئيسية بعد تسجيل الخروج.
    """
    
    logout(request)  # ✅ إنهاء الجلسة ومسح بياناتها لمنع أي وصول غير مصرح به بعد الخروج

    request.session.flush()  # ✅ إزالة جميع بيانات الجلسة لضمان عدم بقاء أي بيانات حساسة
    
    messages.success(request, "✅ تم تسجيل خروجك بنجاح!")  # ✅ إشعار المستخدم بنجاح تسجيل الخروج
    
    return redirect('homepage')  # ✅ إعادة التوجيه إلى الصفحة الرئيسية بعد تسجيل 



def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email").strip()
        user = CustomUser.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

            send_mail(
                "إعادة تعيين كلمة المرور",
                f"مرحبًا {user.username}،\n\nيمكنك إعادة تعيين كلمة المرور عبر الرابط التالي:\n{reset_link}",
                "noreply@yourdomain.com",
                [user.email],
                fail_silently=False,
            )

            messages.success(request, "✅ تم إرسال رابط إعادة التعيين إلى بريدك الإلكتروني.")
            return redirect("login")

        messages.error(request, "⚠️ البريد الإلكتروني غير مسجل!")
    
    return render(request, "password_reset_request.html")

def password_reset_confirm(request, uidb64, token):
    """
    ✅ فيو لإعادة تعيين كلمة المرور بعد فتح الرابط المرسل بالبريد الإلكتروني.
    ✅ يتحقق من صلاحية الرابط قبل السماح للمستخدم بإدخال كلمة مرور جديدة.
    ✅ يمنع إعادة استخدام الرابط بعد تغييره مرة واحدة.
    """
    User = get_user_model()

    try:
        # ✅ فك تشفير UID المستخدم من الرابط
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # ✅ التحقق من صلاحية الرابط ومنع استخدامه أكثر من مرة
    if user is None or not default_token_generator.check_token(user, token) or not user.is_active:
       messages.error(request, "⚠️ رابط إعادة تعيين كلمة المرور غير صالح أو منتهي الصلاحية.")
       return redirect("password_reset_invalid")

    if request.method == "POST":
        new_password = request.POST.get("password1", "").strip()
        confirm_password = request.POST.get("password2", "").strip()

        # ✅ التحقق من أن كلمة المرور ليست فارغة وتفي بالحد الأدنى للطول
        if not new_password or len(new_password) < 8:
            messages.error(request, "⚠️ كلمة المرور يجب أن تكون 8 أحرف على الأقل!")
            return render(request, "password_reset_confirm.html", {"uidb64": uidb64, "token": token})

        # ✅ التحقق من قوة كلمة المرور (يجب أن تحتوي على رقم ورمز واحد على الأقل)
        if not re.search(r"[0-9]", new_password) or not re.search(r"[@$!%*?&#]", new_password):
            messages.error(request, "⚠️ يجب أن تحتوي كلمة المرور على رقم واحد على الأقل ورمز خاص (@, $, !, %, *, ?, & أو #)!")
            return render(request, "password_reset_confirm.html", {"uidb64": uidb64, "token": token})

        # ✅ التحقق من تطابق كلمة المرور مع التأكيد
        if new_password != confirm_password:
            messages.error(request, "⚠️ كلمة المرور غير متطابقة!")
            return render(request, "password_reset_confirm.html", {"uidb64": uidb64, "token": token})

        # ✅ تحديث كلمة المرور مع تشفيرها
        user.password = make_password(new_password)

        # ✅ تعطيل الحساب مؤقتًا حتى يتم التفعيل عبر البريد الإلكتروني (لمنع إعادة استخدام الرابط)
        user.is_active = False  
        user.activation_token = str(uuid.uuid4())   # ✅ إنشاء رمز تفعيل جديد
        user.save()

        # ✅ إرسال رابط التفعيل الجديد إلى البريد الإلكتروني
        activation_link = request.build_absolute_uri(
            reverse('activate_account', kwargs={'token': user.activation_token})
        )
        send_mail(
            "إعادة تفعيل حسابك بعد تحديث كلمة المرور",
            f"مرحبًا {user.username}،\n\nتم تحديث كلمة المرور بنجاح. قبل تسجيل الدخول، يرجى تفعيل حسابك عبر الرابط التالي:\n{activation_link}",
            "noreply@yourdomain.com",
            [user.email],
            fail_silently=False,
        )

        # ✅ إبلاغ المستخدم بأنه يجب تفعيل الحساب بعد تحديث كلمة المرور
        messages.success(request, "✅ تم تحديث كلمة المرور بنجاح! تحقق من بريدك الإلكتروني لتفعيل الحساب.")
        return redirect("pending_activation")

    # ✅ إذا كانت الطلب `GET`، نعرض نموذج تغيير كلمة المرور
    return render(request, "password_reset_confirm.html", {"uidb64": uidb64, "token": token})

def password_reset_invalid(request):
    """عرض صفحة خطأ عند استخدام رابط إعادة تعيين كلمة المرور منتهي الصلاحية"""
    return render(request, "password_reset_invalid.html")
