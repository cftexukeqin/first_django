# 数据模型，前后台都可登录
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from shortuuidfield import ShortUUIDField

class Usermanager(BaseUserManager):
    # 创建用户函数封装
    def _create_user(self,telephone,password,username,**kwargs):
        if not telephone:
            raise ValueError('请输入手机号')
        if not password:
            raise ValueError('请输入密码')
        if not username:
            raise ValueError('请输入用户名')
        user = self.model(telephone=telephone,username=username,**kwargs)
        user.set_password(password)
        user.save()
        return user
    # 定义创建普通用户函数
    def create_user(self,telephone,password,username,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone=telephone,password=password,username=username)
    # 定义创建超级用户的函数
    def create_superuser(self,telephone,password,username,**kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(telephone=telephone,password=password,username=username)


class User(AbstractBaseUser,PermissionsMixin):
    uid = ShortUUIDField(primary_key=True)
    telephone = models.CharField(max_length=11,unique=True)
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']
    # EMAIL_FIELD = 'email'
    objects = Usermanager()
    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username
