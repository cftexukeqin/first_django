from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,reverse
from .models import User
from .forms import LoginForm,SignupForm,SmsCaptchaForm
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate,login,logout
from utils import restful,dxcache
# 图形验证码相关的包
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
# 短信验证码
from utils.alidysmssdk import alidysmssend
@require_POST
def login_view(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')
        user = authenticate(request,telephone=telephone,password=password)
        if user:
            if user.is_active:
                login(request,user)
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                return restful.ok()
            else:
                return restful.noauth(message='该用户已被拉黑')
        else:
            return restful.paramserror(message='手机号或者密码错误')

    else:
        errors = form.get_error()
        print(errors)
        return restful.paramserror(message=errors)
@require_POST
def signup(request):
    form = SignupForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(telephone=telephone,password=password,username=username)
        login(request,user)
        return restful.ok()
    else:
        return restful.paramserror(message=form.get_error())
# 图形验证码
def graph_captcha(request):
    text,image = Captcha.gene_code()
    # BytesIO：相当于一个管道，用来存储图片的流数据
    out = BytesIO()
    # 调用image的save方法，将这个image对象保存到BytesIO中
    image.save(out,'png')
    # 将BytesIO的文件指针移动到最开始的位置
    out.seek(0)

    response = HttpResponse(content_type='image/png')
    # 从BytesIO的管道中，读取出图片数据，保存到response对象上
    response.write(out.read())
    response['Content-length'] = out.tell()

    # 12Df：12Df.lower()
    dxcache.set(text.lower(),text.lower(),5*60)

    return response

# 短信验证码
@require_POST
def sms_captcha(request):
    # telephone = request.GET.get('telephone')
    # code = Captcha.gene_text(number=6)
    # dxcache.set(telephone,code)
    # # result = alidysmssend.send_sms(telephone, code)
    # print(code)
    form = SmsCaptchaForm(request.POST)
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        print(telephone)
        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            return restful.paramserror(message='该手机已被注册！')
        code = Captcha.gene_text(number=6)
        dxcache.set(telephone,code)
        # send_result = alidysmssend.send_sms(telephone,code)
        # if send_result:
        print(code)
        return restful.ok()
        # else:
        #     print(send_result)
        #     return restful.paramserror(message='发送失败')
    else:
        return restful.paramserror(message=form.get_error())


def my_logout(request):
    logout(request)
    return redirect(reverse('index'))
