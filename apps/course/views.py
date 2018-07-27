from django.shortcuts import render
from .models import Course,CourseOrder
# Create your views here.
from django.conf import settings
import hmac,hashlib,os,time
from utils import restful

def course_index(request):
    context = {
        'courses':Course.objects.select_related('teacher','category').all()
    }
    return render(request,'course/course_index.html',context=context)

def course_detail(request,course_id):
    context = {
        'course':Course.objects.select_related('teacher','category').get(pk=course_id)
    }
    return render(request,'course/course_detail.html',context=context)
def course_token(request):
    file = request.GET.get('video')

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


def course_order(request,course_id):
    course = Course.objects.get(pk=course_id)
    order = CourseOrder.objects.filter(course=course)
    context = {
        'course':course,
        'order':order
    }
    return render(request,'course/course_order.html',context=context)