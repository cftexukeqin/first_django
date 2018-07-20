from django.urls import path
from . import views


app_name = 'cms'
urlpatterns =[
    path('',views.index,name='index'),
    path('add_news/',views.AddNewsView.as_view(),name='add_news'),
    path('news_category/',views.news_category,name='news_category'),
    path('news_lists/',views.news_lists,name='news_lists'),
    path('add_category/',views.add_category,name='add_category'),
    path('edit_category/',views.edit_category,name='edit_category'),
    path('del_category/',views.del_category,name='del_category'),
    path('upload_file/',views.upload_file,name='upload_file'),
    path('banner/',views.banner,name='banner'),
    path('banner_list/',views.banner_list,name='banner_list'),
    path('addbanner/',views.addbanner,name='addbanner'),
    path('editbanner/',views.edit_banner,name='editbanner'),
    path('delete_banner/',views.delete_banner,name='delete_banner'),
    path('qntoken/',views.qntoken,name='qntoken'),
]