from django import forms
from apps.forms import FormMixin
from apps.news.models import NewsModel,Banner

class EditNewsCategoryForm(forms.Form,FormMixin):
    pk = forms.CharField(error_messages={'required':'必须输入分类PK'})
    name = forms.CharField(max_length=100)

class NewsForm(forms.ModelForm,FormMixin):
    class Meta:
        model = NewsModel
        fields = ['title','desc','content','thumbnail','category']

class AddBannerForm(forms.ModelForm,FormMixin):
    class Meta:
        model = Banner
        fields = ['priority','image_url','link_to']

class EditBannerForm(forms.ModelForm,FormMixin):
    pk = forms.IntegerField()
    class Meta:
        model = Banner
        fields = ['priority','image_url','link_to']