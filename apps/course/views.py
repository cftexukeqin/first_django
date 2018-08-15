from django.shortcuts import render,reverse
from .models import Course,CourseOrder
# Create your views here.
from django.conf import settings
import hmac,hashlib,os,time
from utils import restful
from apps.xfzauth.decorators import xfz_login_required
from hashlib import md5
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now as now_func
from django.views.decorators.http import require_POST
import datetime

def course_index(request):
    context = {
        'courses':Course.objects.select_related('teacher','category').all()
    }
    return render(request,'course/course_index.html',context=context)

def course_detail(request,course_id):
    course = Course.objects.select_related('teacher', 'category').get(pk=course_id)
    print(request.user)
    buyed = None
    if request.user:
        buyed = CourseOrder.objects.filter(course=course,status=2,buyer=request.user).exists()
    context = {
        'course':course,
        'buyed':buyed
    }
    return render(request,'course/course_detail.html',context=context)


@xfz_login_required
def course_token(request):
    file = request.GET.get('video')
    course_id = request.GET.get('course_id')
    if not CourseOrder.objects.filter(course_id=course_id,status=2,buyer=request.user).exists():
        return restful.paramserror(message='请先购买该课程！')
    expiration_time = int(time.time()) + 2 * 60 * 60

    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    extension = os.path.splitext(file)[1]
    media_id = file.split('/')[-1].replace(extension, '')

    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
    return restful.result(data={'token': token})

@xfz_login_required
def course_order(request,course_id):
    course = Course.objects.get(pk=course_id)
    order = None
    # 判断该用户是否已经创建此订单，如果不存在则创建
    if not CourseOrder.objects.filter(course_id=course.id).exists():
        order = CourseOrder.objects.create(course=course,buyer=request.user,status=1,amount=course.price,expire_time=now_func()+datetime.timedelta(hours=2))
    else:
        # 先判断是否过期
        order = CourseOrder.objects.filter(course_id=course.id,buyer=request.user).first()
        if order.expire_time < now_func():
            #如果已经存在且处于过期，重新选择后将该订单的创建时间和过期时间进行更新。
            CourseOrder.objects.filter(course_id=course_id).update(create_time=now_func(),expire_time=now_func()+datetime.timedelta(hours=2))
    context = {
        'goods':{
            'thumbnail':course.cover_url,
            'price':course.price,
            'title':course.title
        },
        'order':order,
        'notify_url':request.build_absolute_uri(reverse('course:notify_url')),
        'return_url':request.build_absolute_uri(reverse('course:detail',kwargs={'course_id':course.id}))
    }
    return render(request,'course/course_order.html',context=context)

@xfz_login_required
def course_order_key(request):
    goodsname = request.POST.get("goodsname")
    istype = request.POST.get("istype")
    notify_url = request.POST.get("notify_url")
    orderid = request.POST.get("orderid")
    price = request.POST.get("price")
    return_url = request.POST.get("return_url")

    token = 'ae33e898fb82a8085adebc320f7524d6'
    uid = '7b21d7aac9ecec899e9ebeac'
    orderuid = str(request.user.pk)
    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode(
        "utf-8")).hexdigest()
    return restful.result(data={"key": key})

@require_POST
def del_course(request):
    order_id = request.POST.get('order_id')
    print(order_id)
    try:
        order = CourseOrder.objects.get(pk=order_id)
        order.delete()
        return restful.ok()
    except:
        return restful.paramserror(message='该订单不存在！')

@csrf_exempt
def notify_view(request):
    course_id = request.POST.get('orderid')
    CourseOrder.objects.filter(pk=course_id).update(status=2)
    return restful.ok()
