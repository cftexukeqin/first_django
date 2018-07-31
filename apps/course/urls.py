from django.urls import path
from . import views

app_name = 'course'
urlpatterns = [
    path('',views.course_index,name='index'),
    path('<int:course_id>/',views.course_detail,name='detail'),
    # 用于百度云课程播放的token
    path('course_token/',views.course_token,name='course_token'),
    # 课程订单跳转链接
    path('course_order/<int:course_id>/',views.course_order,name='course_order'),
    # 产生course_order_key 的url
    path('course_order_key/',views.course_order_key,name='course_order_key'),
    # notify_url的url
    path('notify_url',views.notify_view,name='notify_url'),
    path('del_course/',views.del_course,name='del_course')
]