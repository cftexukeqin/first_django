from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,Permission,ContentType
from apps.news.models import NewsCategory,NewsModel,Comment
from apps.course.models import Course,CourseCategory,Teacher,CourseOrder
from apps.payinfo.models import Payinfo,PayinfoOrder

class Command(BaseCommand):
    def handle(self, *args, **options):
        # 添加分组
        # 1 编辑组(新闻管理，课程管理)
        # 根据模型获取相应的权限
        edit_content_types = [
            ContentType.objects.get_for_model(NewsModel),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Teacher),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Payinfo),
        ]
        edit_permissions = Permission.objects.filter(content_type__in=edit_content_types)
        editGroup = Group.objects.create(name='编辑')
        editGroup.permissions.set(edit_permissions)
        editGroup.save()
        self.stdout.write(self.style.SUCCESS('创建编辑组成功！'))
        # 2 财务组
        finance_content_types = [
            ContentType.objects.get_for_model(CourseOrder),
            ContentType.objects.get_for_model(PayinfoOrder),
        ]
        finance_permissions = Permission.objects.filter(content_type__in=finance_content_types)
        financeGroup = Group.objects.create(name='财务')
        financeGroup.permissions.set(finance_permissions)
        financeGroup.save()
        self.stdout.write(self.style.SUCCESS('创建财务组成功！'))
        # 3 管理员组，财务+编辑
        admin_permissions = edit_permissions.union(finance_permissions)
        adminGroup = Group.objects.create(name='管理员')
        adminGroup.permissions.set(admin_permissions)
        adminGroup.save()
        self.stdout.write(self.style.SUCCESS('创建管理员成功！'))