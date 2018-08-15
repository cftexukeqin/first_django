from django import template
from datetime import datetime
from django.utils.timezone import localtime
import pytz
from ..models import NewsModel
from django.db.models import Count

register = template.Library()

@register.filter
def time_since(value):
    if isinstance(value,datetime):
        now = datetime.now()
        now = now.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
        timestramp = (now - value).total_seconds()
        if timestramp<60:
            return '刚刚'
        elif timestramp>60 and timestramp<60*60:
            minutes = int(timestramp/60)
            return  '%s分钟前' % minutes
        elif timestramp>60*60 and timestramp<60*60*24:
            hours = int(timestramp/(60*60))
            return '%s小时前' % hours
        elif timestramp>60*60*24 and timestramp <60*60*24*30:
            days = int(timestramp/(60*60*24))
            return '%s天前' % days
        else:
            return value.strftime("%Y-%m-%d %H:%M")
    else:
        return value

@register.filter
def time_format(value):
    if not isinstance(value,datetime):
        return value
    else:
        return localtime(value).strftime("%Y-%m-%d %H:%M:%S")

@register.filter
def time_expire(value):
    now = datetime.now()
    now = now.replace(tzinfo=pytz.timezone('Asia/Shanghai'))
    timest = (now - value).total_seconds()
    if timest < 0:
        return '去支付'
    else:
        return '订单已过期'

#自定义标签，评论最多的新闻
@register.simple_tag
def most_commented_news():
    return NewsModel.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:4]