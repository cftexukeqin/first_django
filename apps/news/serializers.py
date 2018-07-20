from rest_framework import serializers
from .models import NewsCategory,NewsModel,Comment,Banner
from apps.xfzauth.serializers import UserSerializers


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id','name')

class NewsSerializers(serializers.ModelSerializer):
    category = CategorySerializers()
    author = UserSerializers()
    class Meta:
        model = NewsModel
        fields = ('id','title','desc','thumbnail','category','author','pub_time')

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializers()
    class Meta:
        model = Comment
        fields=('id','pub_time','content','author')

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id','priority','image_url','link_to','pub_time')
