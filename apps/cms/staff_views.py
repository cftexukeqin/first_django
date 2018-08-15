from django.urls import include,path
from django.shortcuts import render,reverse,redirect
from apps.xfzauth.models import User
from django.contrib.auth.models import Group
from django.contrib import messages
from django.views.generic import View

def staff(request):
    staffs = User.objects.filter(is_staff=True)
    context = {
        'staffs':staffs
    }
    return render(request,'cms/staffs.html',context=context)

class AddStaffView(View):
    def get(self,request):
        groups = Group.objects.all()
        context = {
            'groups':groups
        }
        return render(request,'cms/add_staff.html',context=context)

    def post(self,request):
        telephone = request.POST.get('telephone')
        if telephone:
            user = User.objects.filter(telephone=telephone).first()
            if user:
                user.is_staff = True
                groups_id = request.POST.getlist('groups')
                groups = Group.objects.filter(id__in=groups_id)
                user.groups.set(groups)
                user.save()
                return redirect(reverse('cms:staff'))
            else:
                messages.info(request,'手机号码不存在')
                return redirect(reverse('cms:add_staff'))
        else:
            messages.error(request, '请输入员工手机号')
            return redirect(reverse('cms:add_staff'))