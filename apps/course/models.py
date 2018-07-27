from django.db import models
from shortuuidfield import ShortUUIDField
# Create your models here.
class CourseCategory(models.Model):
    name = models.CharField(max_length=100)

class Teacher(models.Model):
    username = models.CharField(max_length=100)
    avatar = models.URLField()
    jobtitle = models.CharField(max_length=100)
    profile = models.CharField(max_length=100)

class Course(models.Model):
    title = models.CharField(max_length=100)
    video_url = models.URLField(null=True)
    cover_url = models.URLField()
    price = models.FloatField()
    desc = models.TextField(null=True)
    category = models.ForeignKey('course.CourseCategory',on_delete=models.DO_NOTHING,null=True)
    teacher = models.ForeignKey('course.Teacher',on_delete=models.DO_NOTHING,null=True)
    duration = models.IntegerField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-pub_time']

class CourseOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    buyer = models.ForeignKey('xfzauth.User',on_delete=models.DO_NOTHING)
    course = models.ForeignKey('course.Course',on_delete=models.DO_NOTHING)
    amount = models.FloatField(default=0)
    #订单支付状态，默认1为未支付，2为已支付
    status = models.SmallIntegerField(default=1)
    #支付方式，1为支付宝，2为微信
    istype = models.SmallIntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_time']