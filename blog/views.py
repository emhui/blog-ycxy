from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.
from .models import Post,Category,Tag
from comments.forms import CommentForm
import markdown
from django.views.generic import ListView, DetailView

def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request,'blog/index.html',context={
        'title':'首页',
        'welcome':'这是第一个页面',
        'post_list':post_list,
    })

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 3

def detail(request, pk):
    post = get_object_or_404(Post,pk=pk)

    # 增加评论数
    post.increase_views()
    post.body = markdown.markdown(
        post.body,
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    # 导入from表单
    form = CommentForm()
    # 获取所有评论并且显示
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form':form,
        'comment_list':comment_list,
    }

    return render(request,'blog/detail.html',context=context)

def archive(request, year, month):
    post_list = Post.objects.filter(
        created_time__year = year,
        created_time__month = month,
    ).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

def category(request, pk):
    category = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=category).order_by('-created_time')
    return render(request,'blog/index.html',context={'post_list':post_list})

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month
                                                               )

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    # 重写get方法，在里面添加 increase_views()方法
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request,*args, **kwargs)
        self.object.increase_views()
        return response

    # 对object对象进行渲染
    def get_object(self, queryset=None):
        post = super(PostDetailView,self).get_object(queryset=None)
        post.body = markdown.markdown(
            post.body,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        return post
    # 处理表单,传递其他的数据
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        # 导入from表单
        form = CommentForm()
        # 获取所有评论并且显示
        comment_list = self.object.comment_set.all()
        context = {
            'form': form,
            'comment_list': comment_list,
        }

        return context

def about(request):
    return render(request,'about.html')

def more(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/more.html', context={
        'title': '首页',
        'welcome': '这是第一个页面',
        'post_list': post_list,
    })