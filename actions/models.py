from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    """定义一个动作模型"""
    user = models.ForeignKey(User, related_name='actions', db_index=True)  # db_index： 为这个字典创建索引
    verb = models.CharField(max_length=255)  # 执行操作的描述
    created = models.DateField(auto_now_add=True, db_index=True)
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='object_obj')
    target_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{}{}{}'.format(self.user, self.verb, self.target)
