from django.shortcuts import render
from .forms import LoginForm, UserRegistrationForm, UserForm, ProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact  # 用这个中间模型来创建用户关系
from actions.utils import create_action
from actions.models import Action
# Create your views here.


@login_required
def dashboard(request):
    actions = Action.objects.exclude(user=request.user)  # 获取除了自己之外的所有用户动作
    following_ids = request.user.following.values_list('id', flat=True)  # 取得所有请求用户关注人的id
    if following_ids:
        actions = Action.objects.filter(user_id__in=following_ids)\
            .select_related('user', 'user__profile').prefetch_related('target')  # 过滤取得关注人的动作
    actions = actions[:10]  # 如果没关注任何人就显示所有用户的动作10条 关注了就显示关注用户的
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'actions': actions})  # section变量跟踪用户正在查看的页面


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # 新建一个用户但是不立马保存到数据库
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            create_action(new_user, "has created an account")
            profile = Profile.objects.create(user=new_user)
            # 定向到注册成功页面
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserForm(instance=request.user,data=request.POST)
        profile_form = ProfileForm(instance=request.user.profile,
                                   data=request.POST,
                                   files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updated your profile')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})


@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id).filter(is_active=True)   # 获取激活状态的用户
    return render(request, 'account/user/list.html',
                  {'section': 'people',
                   'users': users})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html',
                  {'section': 'people',
                   'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user)
                create_action(request.user, " is following", user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ko'})
    return JsonResponse({'status': 'ko'})