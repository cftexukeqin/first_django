from django.urls import path
from . import views

# 应用命名空间
app_name = 'news'

urlpatterns =[
    path('<int:news_id>/',views.news_detail,name='detail'),
    path('list/',views.news_list,name='list'),
    path('pub_comment/',views.pub_comment,name='pub_comment'),
]