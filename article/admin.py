from django.contrib import admin

# Register your models here.
from . import models
from .models import ArticleColumn

admin.site.register(models.AriticlePost)
# 注册文章栏目
admin.site.register(ArticleColumn)