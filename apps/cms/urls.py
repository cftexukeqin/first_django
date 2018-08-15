from django.urls import path
from . import views
from . import course_views
from . import staff_views
app_name = 'cms'

urlpatterns =[
    path('',views.index,name='index'),
    path('add_news/',views.AddNewsView.as_view(),name='add_news'),
    path('news_category/',views.news_category,name='news_category'),
    path('news_lists/',views.NewsListView.as_view(),name='news_lists'),
    path('edit_news/',views.EditNews.as_view(),name='edit_news'),
    path('del_news/',views.del_news,name='del_news'),
    path('add_category/',views.add_category,name='add_category'),
    path('edit_category/',views.edit_category,name='edit_category'),
    path('del_category/',views.del_category,name='del_category'),
    path('upload_file/',views.upload_file,name='upload_file'),
    path('banner/',views.banner,name='banner'),
    path('banner_list/',views.banner_list,name='banner_list'),
    path('addbanner/',views.addbanner,name='addbanner'),
    path('editbanner/',views.edit_banner,name='editbanner'),
    path('delete_banner/',views.delete_banner,name='delete_banner'),
    path('comments/',views.comments,name='comments'),
    path('qntoken/',views.qntoken,name='qntoken'),
]
#course路由
urlpatterns += [
    path('add_course/',views.CourseView.as_view(),name='add_course'),
    path('course_list/',views.course_lists,name='course_list'),
    path('add_course_category/',views.AddCourseCategoryView.as_view(),name='add_course_category'),
    path('del_course_category/',course_views.del_course_category,name='del_course_category'),
    path('edit_course_category/',course_views.edit_category,name='edit_course_category'),

]
# staff路由
urlpatterns += [
    path('staff/',staff_views.staff,name='staff'),
    path('add_staff/',staff_views.AddStaffView.as_view(),name='add_staff')
]

