from django.db import models

# Create your models here.

from shortuuidfield import ShortUUIDField

class Payinfo(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    price = models.FloatField()
    path = models.FilePathField()

class PayinfoOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    buyer = models.ForeignKey('xfzauth.User',on_delete=models.DO_NOTHING)
    payinfo = models.ForeignKey('payinfo.Payinfo',related_name='order',on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    #订单支付状态，默认1为未支付，2为已支付
    status = models.SmallIntegerField(default=1)
    #支付方式，1为支付宝，2为微信
    istype = models.SmallIntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(null=True)

    class Meta:
        ordering = ['-create_time']