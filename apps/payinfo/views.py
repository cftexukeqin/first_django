from django.shortcuts import render,reverse
from .models import Payinfo,PayinfoOrder
import datetime,os
from django.utils.timezone import now as now_func
from django.conf import settings
from utils import restful
from apps.xfzauth.decorators import xfz_login_required
from django.http import FileResponse
from django.http.response import Http404
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def payinfo(request):
    payinfos = Payinfo.objects.all()
    context = {
        'payinfos':payinfos
    }
    return render(request,'payinfo/payinfo.html',context=context)

@xfz_login_required
def payinfo_order(request):
    payinfo_id = request.GET.get('payinfo_id')
    payinfo = Payinfo.objects.get(pk=payinfo_id)
    order = None
    # 判断订单是否存在
    if not PayinfoOrder.objects.filter(payinfo=payinfo,buyer=request.user).exists():
        # 不存在就新建订单
        PayinfoOrder.objects.create(payinfo=payinfo,buyer=request.user,amount=payinfo.price,expire_time=now_func()+datetime.timedelta(hours=settings.EXPIER_TIME))
    else:
        # 如果存在，判断是否过期，如果已经过期，则将该订单的创建时间和过期时间更新。不再重新创建订单
        order = PayinfoOrder.objects.filter(payinfo=payinfo,buyer=request.user).first()
        if order.expire_time < now_func():
            PayinfoOrder.objects.filter(payinfo=payinfo,buyer=request.user).update(create_time=now_func(),expire_time=now_func()+datetime.timedelta(hours=settings.EXPIER_TIME))

    context = {
        'goods':{
            'thumbnail':"",
            'title':payinfo.title,
            'price':payinfo.price
        },
        'order':order,
        'notify_url':request.build_absolute_uri(reverse('payinfo:notify_url')),
        'return_url':request.build_absolute_uri(reverse('payinfo:payinfo'))
    }
    return render(request,'course/course_order.html',context=context)

@xfz_login_required
def down_file(request):
    # 获取payinfo的ID，下载数据
    payinfo_id = request.GET.get('payinfo_id')
    order = PayinfoOrder.objects.filter(payinfo_id=payinfo_id,buyer=request.user,status=2).first()
    if order:
        payinfo = order.payinfo
        path = payinfo.path
        # 打开该文件
        fp = open(os.path.join(settings.MEDIA_ROOT,path),'rb')
        # print(os.path.join(settings.MEDIA_ROOT,path))
        # 获取文件名称
        filename = path.split('/')[-1]
        # 创建一个文件的返回对象
        response = FileResponse(fp)
        # 设置文件格式
        response['Content-Type'] = 'image/jpeg'
        # 以下载的方式
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
        return response
    else:
        return Http404()

# 付款成功的回调函数
@csrf_exempt
def notify_view(request):
    # 回调函数的参数是orderid
    order_id = request.POST.get('orderid')
    PayinfoOrder.objects.filter(pk=order_id).update(status=2)
    return restful.ok()