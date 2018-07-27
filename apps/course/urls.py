from django.urls import path
from . import views

app_name = 'course'
urlpatterns = [
    path('',views.course_index,name='index'),
    path('<int:course_id>/',views.course_detail,name='detail'),
    path('course_token/',views.course_token,name='course_token'),
    path('course_order/<course_id>/',views.course_order,name='course_order')
]