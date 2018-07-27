from django import forms
from apps.forms import FormMixin
from apps.news.models import NewsModel,Banner
from apps.course.models import Course,CourseCategory,Teacher
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

class EditNewsForm(forms.ModelForm,FormMixin):
    pk = forms.IntegerField()
    class Meta:
        model = NewsModel
        fields = ['title','desc','content','thumbnail','category']

class DelNewsForm(forms.Form,FormMixin):
    pk = forms.IntegerField()

class CourseForm(forms.ModelForm,FormMixin):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()
    class Meta:
        model = Course
        fields = ['title','price','duration','desc','video_url','cover_url']

class AddCourseCategoryForm(forms.ModelForm,FormMixin):
    class Meta:
        model = CourseCategory
        fields =['name']