from django.shortcuts import render,redirect,reverse
from apps.course.models import CourseCategory
from utils import restful

def edit_category(request):
    pk = request.POST.get('pk')
    name = request.POST.get('name')
    try:
        CourseCategory.objects.filter(pk=pk).update(name=name)
        return restful.ok()
    except:
        return restful.paramserror(message='参数错误！')

def del_course_category(request):
    category_id = request.POST.get('pk')
    try:
        category = CourseCategory.objects.get(pk=category_id)
        category.delete()
        return restful.ok()
    except:
        return restful.paramserror(message='这个分类不存在!')