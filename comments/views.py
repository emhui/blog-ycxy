from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
from .models import Comment
from .forms import CommentForm
from blog.models import Post
from .models import Comment

def post_comment(request, pk):
    # 1. 获取当前对应的文章对象
    post = get_object_or_404(Post,pk=pk)
    # 2. 判断当前方法
    if request.method == 'POST':
        # 3. 获取表单
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post) # 重定向到post页面

        else:
            comment_list = post.comment_set.all()
            context = {
                'post':post,
                'form':form,
                'comment_list':comment_list,
            }
            return render(request,'blog/detail',context=context)
    else:
        return redirect(post)