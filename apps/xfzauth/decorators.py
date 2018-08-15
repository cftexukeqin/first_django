from django.shortcuts import redirect
from utils import restful

def xfz_login_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
           return func(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return restful.noauth(message='登陆后才能评论')
            else:
                return redirect('/')
            # return restful.noauth(message='请先登录！')
    return wrapper