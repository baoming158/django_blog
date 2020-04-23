from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from article.models import AriticlePost

# 博文的评论
class Comment(MPTTModel):
    # 新增，mptt树形结构
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    article = models.ForeignKey(
        AriticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    # body = models.TextField()
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['created']

    def __str__(self):
        return self.body[:20]

