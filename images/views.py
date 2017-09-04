from django.shortcuts import render, redirect, get_object_or_404
from .forms import ImageCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Image
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from common.decorators import ajax_required
from actions.utils import create_action


@login_required
def image_create(request):
    """创建图片的视图 通过点击一个javascript书签"""
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, "bookmarked image", new_image)
            messages.success(request, "Image added successfully")
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)  # GET请求带url地址
    return render(request, 'images/image/create.html', {'form': form})


@login_required
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section': 'images',
                                                        'image': image})


def get_image_likes(image):
    user_username = [i.username for i in image.user_like.all()]
    user_first_name = [i.first_name for i in image.user_like.all()]
    user_photo_url = [i.profile.photo.url for i in image.user_like.all()]
    result = {i: [j, k] for i, j, k in zip(user_username, user_first_name, user_photo_url)}
    return result


@ajax_required
@require_POST
@login_required
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    # 获取ajax提交的id跟动作后从模型取得实例
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
                create_action(request.user, "likes", image)

            else:
                image.user_like.remove(request.user)
            user_dict = get_image_likes(image)
            return JsonResponse(user_dict)
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)  # 如果获取到page页码不是证书 获取第一页图片实例
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html',
                      {"section": 'images', "images": images})  # 返回一段html
    return render(request, 'images/image/list.html',
                  {'section': 'images', 'images': images})


