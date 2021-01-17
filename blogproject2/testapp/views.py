from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from testapp.models import Post
from testapp.models import Comment
from testapp.forms import CommentForm
#from taggit.models import Tag
# Create your views here.
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    #tag=None
    #if tag_slug:
    #    tag=get_object_or_404(Tag,slug=tag_slug)
    #    post_list=post_list.filter(tags__in=[tag])

    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page')
    try:
       post_list=paginator.page(page_number)
    except PageNotAnInteger:
       post_list=paginator.page(1)
    except EmptyPage:
       post_list=paginator.page(paginator.num_pages)
    return render(request,'testapp/post_list.html',{'post_list':post_list,})



from django.views.generic import ListView
class PostListView(ListView):
    model=Post
    paginate_by=2

def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(data=request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()
    return render(request,'testapp/post_detail.html',{'post':post,'form':form,'comments':comments,'csubmit':csubmit})


# Create your views here.