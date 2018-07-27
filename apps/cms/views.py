from django.shortcuts import render,redirect,reverse
from django.views.generic import View
from django.views.decorators.http import require_POST,require_GET
from apps.news.models import NewsCategory,NewsModel,Banner,Comment
from .forms import EditNewsCategoryForm,NewsForm,AddBannerForm,EditBannerForm,DelNewsForm,EditNewsForm,CourseForm,AddCourseCategoryForm
from apps.news.serializers import BannerSerializer
from django.core.paginator import Paginator
from apps.course.models import Course,Teacher,CourseCategory
from utils import restful
from datetime import  datetime
from django.utils.timezone import make_aware
from urllib import parse
from ..xfzauth.models import User
import qiniu
import os
from django.conf import settings
# Create your views here.
def index(request):
    return render(request,'cms/index.html')

@require_GET
def news_category(request):
    categories = NewsCategory.objects.all()
    context = {
        'categories':categories
    }
    return render(request, 'cms/news_category.html', context=context)

class AddNewsView(View):
    def get(self,request):
        categories = NewsCategory.objects.all()
        context = {
            'categories':categories
        }
        return render(request,'cms/add_news.html',context=context)
    def post(self,request):
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return restful.ok()
        else:
            print(form.get_error())
            return restful.paramserror(message=form.get_error())
@require_POST
def add_category(request):
    category = request.POST.get('category')
    exists = NewsCategory.objects.filter(name=category).exists()
    if not exists:
        NewsCategory.objects.create(name=category)
        return restful.ok()
    else:
        return restful.paramserror(message='该分类已经存在！')

@require_POST
def edit_category(request):
    form = EditNewsCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.paramserror(message=form.get_error())

@require_POST
def del_category(request):
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.paramserror(message='此分类不存在！')

@require_POST
def upload_file(request):
    file = request.FILES.get('file')
    name = file.name
    with open(os.path.join(settings.MEDIA_ROOT,name),'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL+name)
    return restful.result(data={'url':url})

def banner(request):
    return render(request,'cms/banners.html')

def banner_list(request):
    banners = Banner.objects.all()
    serializers = BannerSerializer(banners,many=True)
    data = serializers.data
    return restful.result(data=data)

def addbanner(request):
    form = AddBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        banner = Banner.objects.create(priority=priority,image_url=image_url,link_to=link_to)
        return restful.result(data={'banner_id':banner.pk})
    else:
        print(form.get_error())
        return restful.paramserror(message=form.get_error())

def edit_banner(request):
    form = EditBannerForm(request.POST)
    if form.is_valid():
        priority = form.cleaned_data.get('priority')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        pk = form.cleaned_data.get('pk')
        Banner.objects.filter(pk=pk).update(priority=priority,image_url=image_url,link_to=link_to)
        return restful.ok()
    else:
        print(form.get_error())
        return restful.paramserror(message=form.get_error())
def delete_banner(request):
    bannerId = request.POST.get('banner_id')
    try:
        banner = Banner.objects.get(pk=bannerId)
        banner.delete()
        return restful.ok()
    except:
        return restful.paramserror(message='删除轮播图失败！')
# 生成七牛token
def qntoken(request):
    access_key = 'qHC83yOGuWzpW9hW6Wt2JEQseqKIq0Z4G970ALR9'
    secret_key = 'cnCE1B7T3Jj5tqG1rqisAD2KY6Jz4zSioQCZ_L__'

    q = qiniu.Auth(access_key,secret_key)
    bucket = 'dxxfz'

    token = q.upload_token(bucket)
    return restful.result(data={'token':token})

# def news_lists(request):
#     news_lists = NewsModel.objects.select_related('category','author').all()
#     context = {
#         'news_lists':news_lists,
#         'categories':NewsCategory.objects.all()
#     }
#     return render(request,'cms/news_lists.html',context=context)

class NewsListView(View):
    def get(self,request):
        newses = NewsModel.objects.select_related('category', 'author')
        page = int(request.GET.get('p',1))
        start = request.GET.get('start')
        end = request.GET.get('end')
        category_id = int(request.GET.get('category',0) or 0)
        title = request.GET.get('title')
        print(title)
        if start or end:
            if start:
                start_date = datetime.strptime(start,'%Y/%m/%d')
            else:
                start_date = datetime(year=2018,month=6,day=1)
            if end:
                end_date = datetime.strptime(end,'%Y/%m/%d')
            else:
                end_date = datetime.today()
            newses = newses.filter(pub_time__range=(make_aware(start_date),make_aware(end_date)))
        if title:
            newses = newses.filter(title__icontains=title)
        if category_id:
            newses = newses.filter(category=category_id)
        paginator = Paginator(newses,5)
        page_obj = paginator.page(page)
        context_data = self.get_content_data(paginator,page_obj)
        context = {
            'news_lists':page_obj.object_list ,
            'categories': NewsCategory.objects.all(),
            'paginator':paginator,
            'page_obj':page_obj,
            'url_query':'&'+parse.urlencode({
                'start':start or '',
                'end':end or "",
                'category':category_id or "",
                'title':title or '',
            }),
            'start':start,
            'end':end,
            'title':title,
            'category_id':category_id
        }
        print(context['url_query'])
        context.update(context_data)
        return render(request, 'cms/news_lists.html', context=context)

    def get_content_data(self, paginator, page_obj, arroud_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        left_have_more = False
        right_have_more = False

        if current_page <= arroud_count + 2:
            left_pages = range(1, current_page)
        else:
            left_have_more = True
            left_pages = range(current_page - arroud_count, current_page)

        if current_page >= num_pages - 2 - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_have_more = True
            right_pages = range(current_page + 1, current_page + arroud_count + 1)
        context = {
            'current_page': current_page,
            'left_pages': left_pages,
            'right_pages': right_pages,
            'left_have_more': left_have_more,
            'right_have_more': right_have_more,
            'num_pages': num_pages
        }
        return context
class EditNews(View):
    def get(self,request):
        id = request.GET.get('id')
        news = NewsModel.objects.get(pk=id)
        context = {
            'news':news,
            'categories':NewsCategory.objects.all()
        }
        return render(request,'cms/add_news.html',context=context)
    def post(self,request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('pk')
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            content = form.cleaned_data.get('content')
            thumbnail = form.cleaned_data.get('thumbnail')
            category = form.cleaned_data.get('category')
            NewsModel.objects.filter(pk=pk).update(title=title,desc=desc,content=content,category=category,thumbnail=thumbnail)
            return restful.ok()
        else:
            return restful.paramserror(message=form.get_error())

def del_news(request):
    form = DelNewsForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        news = NewsModel.objects.get(pk=pk)
        news.delete()
        return restful.ok()
    else:
        print(form.get_error())
        return restful.paramserror(message=form.get_error())

def comments(request):
    comments = Comment.objects.select_related('author','news').all()
    context = {
        'comments':comments
    }
    return render(request,'cms/comments_list.html',context=context)

class CourseView(View):
    def get(self,request):
        teachers = Teacher.objects.all()
        categories = CourseCategory.objects.all()
        context = {
            'teachers': teachers,
            'categories': categories
        }
        return render(request, 'cms/add_course.html', context=context)
    def post(self,request):
        form = CourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            category_id = form.cleaned_data.get('category_id')
            teacher_id = form.cleaned_data.get('teacher_id')
            price = form.cleaned_data.get('price')
            duration = form.cleaned_data.get('duration')
            video_url = form.cleaned_data.get('video_url')
            cover_url =form.cleaned_data.get('cover_url')
            desc = form.cleaned_data.get('desc')
            category = CourseCategory.objects.get(pk=category_id)
            teacher = Teacher.objects.get(pk=teacher_id)
            Course.objects.create(title=title,teacher=teacher,category=category,price=price,desc=desc,duration=duration,video_url=video_url
                                  ,cover_url=cover_url)
            return restful.ok()
        else:
            print(form.get_error())
            return restful.paramserror(message=form.get_error())

def course_lists(request):
    courses = Course.objects.all()
    context = {
        'courses':courses
    }
    return render(request,'cms/course_lists.html',context=context)
class AddCourseCategoryView(View):
    def get(self,request):
        context = {
            'categories': CourseCategory.objects.all()
        }
        return render(request, 'cms/add_course_category.html', context=context)
    def post(self,request):
        form = AddCourseCategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            CourseCategory.objects.create(name=name)
            return restful.ok()
        else:
            return restful.paramserror(message=form.get_error())


