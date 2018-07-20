from django.shortcuts import render,redirect,reverse
from django.views.generic import View
from django.views.decorators.http import require_POST,require_GET
from apps.news.models import NewsCategory,NewsModel,Banner
from .forms import EditNewsCategoryForm,NewsForm,AddBannerForm,EditBannerForm
from apps.news.serializers import BannerSerializer
from utils import restful
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

def news_lists(request):
    news_lists = NewsModel.objects.all()
    context = {
        'news_lists':news_lists
    }
    return render(request,'cms/news_lists.html',context=context)