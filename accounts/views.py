from django.shortcuts import render, redirect  # استيراد الأدوات اللازمة لعرض القوالب وإعادة التوجيه
from django.contrib.auth import login  # استيراد `login` لتسجيل دخول المستخدم بعد التسجيل
from .forms import CustomUserCreationForm  # استيراد نموذج التسجيل المخصص

def homepage(request):
    """
    الصفحة الرئيسية لموقع مجتمع الأمن السيبراني
    - يتم عرضها عند دخول الموقع بدون تسجيل دخول
    """
    return render(request, 'homepage.html')  # التأكد من وجود `homepage.html` داخل مجلد `templates`

def dashboard(request):
    """
    الصفحة الرئيسية بعد تسجيل الدخول
    - يمكن تخصيصها لعرض بيانات المستخدم لاحقًا
    """
    return render(request, 'dashboard.html')  # التأكد من وجود `dashboard.html` داخل مجلد `templates`

def register(request):
    """
    صفحة تسجيل مستخدم جديد:
    - إذا كان الطلب `POST`، يتم التحقق من صحة البيانات وحفظ المستخدم
    - إذا كان الطلب `GET`، يتم عرض النموذج فقط دون معالجة البيانات
    - يتم تسجيل دخول المستخدم تلقائيًا بعد نجاح التسجيل
    - يتم تمرير رسائل الخطأ إلى القالب ليتم عرضها في الصفحة بشكل مباشر
    """
    if request.method == 'POST':  # التحقق مما إذا كان الطلب `POST`
        form = CustomUserCreationForm(request.POST, request.FILES)  # تعبئة النموذج بالبيانات المرسلة من المستخدم
        if form.is_valid():  # التحقق من صحة البيانات المدخلة
            user = form.save()  # حفظ المستخدم الجديد في قاعدة البيانات
            login(request, user)  # تسجيل دخول المستخدم تلقائيًا بعد نجاح التسجيل
            return redirect('dashboard')  # إعادة توجيه المستخدم إلى الصفحة الرئيسية بعد التسجيل
    else:
        form = CustomUserCreationForm()  # إنشاء نموذج فارغ عند زيارة الصفحة بدون إرسال بيانات

    return render(request, 'register.html', {'form': form})  # تمرير النموذج إلى القالب ليتم عرضه في واجهة المستخدم
