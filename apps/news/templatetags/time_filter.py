from django import template
from datetime import datetime
import pytz

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