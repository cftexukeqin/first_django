from django import template
register = template.Library()
from apps.payinfo.models import PayinfoOrder

@register.filter
def is_buyed(payinfo,user):
    if user.is_authenticated:
        order = PayinfoOrder.objects.filter(payinfo=payinfo,buyer=user,status=2).exists()
        return order
    else:
        pass