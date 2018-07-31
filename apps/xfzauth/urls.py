from django.urls import path
from . import views

app_name = 'xfzauth'

urlpatterns = [
    path('login/',views.login_view,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.my_logout,name='logout'),
    path('img_captcha/',views.graph_captcha,name='img_captcha'),
    path('sms_captcha/',views.sms_captcha,name='sms_captcha'),
    path('order/',views.my_order,name='order')
]