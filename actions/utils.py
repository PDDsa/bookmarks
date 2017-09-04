import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .models import Action


def create_action(user, verb, target=None):
    """创建一个动作"""
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb=verb,
                                            created__gte=last_minute)  # 创建时间大于一分钟前的所有实例
    if target:
        target_ct = ContentType.objects.get_for_model(target)  # 如果目标存在 获取目标实例
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)  # 在里面检测这个操作是不是在一分钟前
    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)  # 如果不是相似操作 保存实例
        action.save()
        return True
    return False
