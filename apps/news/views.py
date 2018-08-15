from django.shortcuts import render
from django.db.models import Q
from .models import NewsModel,NewsCategory,Comment,Banner
from django.conf import settings
from utils import restful
from .serializers import NewsSerializers,CommentSerializer
from django.http import Http404
from .forms import CommentForm
from apps.xfzauth.decorators import xfz_login_required
import redis
# Create your views here.

# 连接本地redis
from django.conf import settings
xfzredis = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)

def index(request):
    newses = NewsModel.objects.select_related('author','category').all()[0:5]
    categories = NewsCategory.objects.all()
    banners = Banner.objects.all()
    context = {
        'newses':newses,
        'categories':categories,
        'banners':banners
    }

    return render(request,'news/index.html',context=context)

# 使用REST API,以Json 格式返回数据
def news_list(request):
    page = int(request.GET.get('p',1))
    category_id = int(request.GET.get('category_id',0))

    start = (page-1)*settings.PERPAGE_NEWS_COUNT
    end = start+settings.PERPAGE_NEWS_COUNT
    if category_id == 0:
        newses = NewsModel.objects.select_related('author','category').all()[start:end]
    else:
        newses = NewsModel.objects.select_related('author','category').filter(category_id=category_id)[start:end]
    serializers = NewsSerializers(newses,many=True)
    data = serializers.data
    return restful.result(data=data)

def news_detail(request,news_id):
    try:
        news = NewsModel.objects.get(pk=news_id)
        # d通过redis设置访问次数
        total_views = xfzredis.incr('news:{}:views'.format(news.pk))
        xfzredis.zincrby('news_ranking',news.id,1)
        # print(xfzredis.get('news_ranking'))
        # 获取排名前3的新闻
        news_ranking = xfzredis.zrange('news_ranking',0,-1,desc=True)[:4]
        news_ranking_ids = [int(id) for id in news_ranking]
        most_viewed = list(NewsModel.objects.filter(id__in=news_ranking_ids))
        most_viewed.sort(key=lambda x:news_ranking_ids.index(x.id))
        context = {
            'news': news,
            'total_views':total_views,
            'most_viewed':most_viewed
        }
        return render(request, 'news/news_detail.html', context=context)
    except news.DoesNotExist:
        raise Http404

@xfz_login_required
def pub_comment(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')
        news = NewsModel.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content,news=news,author=request.user)
        serializer = CommentSerializer(comment)
        return restful.result(data=serializer.data)
    else:
        return restful.paramserror(form.get_error())

def search(request):
    q = request.GET.get('q')
    context = {}
    if q:
        newses = NewsModel.objects.filter(Q(title__contains=q)|Q(content__contains=q))
        context = {
            'newses':newses
        }
    return render(request, 'search/search.html')

