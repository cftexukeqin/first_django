from django.db import models

# Create your models here.
class NewsCategory(models.Model):
    name = models.CharField(max_length=100)

class NewsModel(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('news.NewsCategory',on_delete=models.SET_NULL,null=True)
    author = models.ForeignKey('xfzauth.User',on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering = ['-pub_time']

class Comment(models.Model):
    content = models.CharField(max_length=500)
    origin_comment = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    pub_time = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey('news.NewsModel',on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey('xfzauth.User',on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']

class Banner(models.Model):
    priority = models.IntegerField()
    image_url = models.URLField()
    link_to = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority']