from django.utils.timezone import now  # ✅ استيراد `now` لجلب الوقت الحالي
from django.conf import settings  # ✅ استيراد `settings` للوصول إلى إعدادات Django
from django.shortcuts import redirect  # ✅ استيراد `redirect` لإعادة توجيه المستخدم بعد تسجيل الخروج
from django.contrib.auth import logout  # ✅ استيراد `logout` لإنهاء جلسة المستخدم
from django.contrib import messages  # ✅ استيراد `messages` لإظهار رسالة تنبيه عند تسجيل الخروج
import datetime  # ✅ استيراد `datetime` لمعالجة القيم الزمنية

class AutoLogoutMiddleware:
    """
    ✅ ميدل وير (Middleware) يقوم بتسجيل خروج المستخدم تلقائيًا بعد فترة معينة من عدم النشاط.
    - يتحقق من نشاط المستخدم عند كل طلب (`request`).
    - إذا تجاوز المستخدم المهلة الزمنية المحددة (`SESSION_COOKIE_AGE`)، يتم تسجيل خروجه.
    - يتم مسح بيانات الجلسة بالكامل لحماية الخصوصية.
    - يتم إعادة توجيه المستخدم إلى الصفحة الرئيسية مع إظهار رسالة توضيحية.
    """

    def __init__(self, get_response):
        """
        ✅ يتم استدعاء هذا المُهيئ (`__init__`) عند تحميل الميدل وير.
        - `get_response`: يُستخدم لمعالجة الطلبات القادمة.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        ✅ يتم تنفيذ هذه الدالة مع كل طلب (`request`) يُرسله المستخدم إلى السيرفر.
        - يتم التحقق من حالة الجلسة ومدة عدم النشاط.
        - يتم تسجيل خروج المستخدم إذا تجاوز مدة الخمول المسموح بها.
        """

        if request.user.is_authenticated:  # ✅ التأكد من أن المستخدم مسجل الدخول
            last_activity_str = request.session.get('last_activity')  # ⏳ جلب وقت آخر نشاط كمحتوى نصي

            if last_activity_str:
                try:
                    # 🕒 تحويل النص المخزن إلى `datetime` من `ISO format`
                    last_activity = datetime.datetime.fromisoformat(last_activity_str)

                    # 🔄 حساب مدة الخمول بالثواني
                    inactive_duration = (now() - last_activity).total_seconds()

                    # ✅ التحقق مما إذا كانت مدة الخمول تجاوزت المهلة المسموح بها
                    if inactive_duration > settings.SESSION_COOKIE_AGE:
                        logout(request)  # ❌ تسجيل خروج المستخدم
                        request.session.flush()  # 🔴 حذف جميع بيانات الجلسة لحماية الخصوصية
                        messages.warning(request, "⚠️ تم تسجيل خروجك تلقائيًا بسبب عدم النشاط لمدة طويلة.")  
                        return redirect('homepage')  # 🔄 إعادة توجيه المستخدم إلى الصفحة الرئيسية

                except ValueError:
                    # 🔄 في حالة حدوث خطأ في التحويل، نعيد ضبط الوقت
                    request.session['last_activity'] = now().isoformat()

            # ⏳ تحديث وقت آخر نشاط للمستخدم وتحويله إلى `ISO format`
            request.session['last_activity'] = now().isoformat()

        return self.get_response(request)  # ✅ السماح بتمرير الطلب إلى التطبيق إذا لم يكن هناك تسجيل خروج
