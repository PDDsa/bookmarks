from django.db import models
from django.conf import settings
from uuslug import slugify
from django.core.urlresolvers import reverse


# Create your models here.


class Image(models.Model):
    """图片模型"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created')  # 图片关联的用户
    title = models.CharField(max_length=125)
    slug = models.SlugField(max_length=200, blank=True)  # 一个只包含数字字母下划线连字符的短标签
    url = models.URLField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    created = models.DateField(auto_now_add=True,
                               db_index=True)  # db_index=Ture Django 将会为这个字段创建索引
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='images_liked',
                                       blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=(self.id, self.slug))
