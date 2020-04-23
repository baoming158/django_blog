from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from comment.forms import CommentForm
from comment.models import Comment
from .models import AriticlePost, ArticleColumn
import markdown
from .forms import ArticlePostForm


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')
    # 初始化查询集
    article_list = AriticlePost.objects.all()

    # 搜索查询集
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''

    # 栏目查询集
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)

    # 标签查询集
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])

    # 查询集排序
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')

    paginator = Paginator(article_list, 3)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {
        'articles': articles,
        'order': order,
        'search': search,
        'column': column,
        'tag': tag,
    }

    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = AriticlePost.objects.get(id=id)

    # 取出文章评论
    comments = Comment.objects.filter(article=id)

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])

    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )

    article.body = md.convert(article.body)

    # 引入评论表单
    comment_form = CommentForm()
    # 添加comments上下文
    context = {'article': article,
               'toc': md.toc,
               'comments': comments,
               'comment_form': comment_form,
               }
    return render(request, 'article/detail.html', context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(request.POST, request.FILES)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            if request.FILES.get('avatar'):
                new_article.avatar = request.FILES.get('avatar')
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])

            # new_article.tags.set(*request.POST.get('tags').split(','), clear=True)
            new_article.save()
            article_post_form.save_m2m()
            return redirect('article:article_list')
        else:
            return HttpResponse('表单提交有误')

    else:
        article_post_form = ArticlePostForm()
        # 新增及修改的代码
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form, 'columns': columns}
        return render(request, 'article/create.html', context)


def article_delete(request, id):
    article = AriticlePost.objects.get(id=id)
    article.delete()
    return redirect('article:article_list')


# 安全删除文章
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request, id):
    # 过滤非作者的用户
    article = AriticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    if request.method == 'POST':
        article = AriticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


# 更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = AriticlePost.objects.get(id=id)

    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 新增及修改的代码
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
            'tags': ','.join([x for x in article.tags.names()]),
        }
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)


class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = AriticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')