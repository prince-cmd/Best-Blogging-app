from django.shortcuts import render, HttpResponse ,redirect
from blog.models import Post , BlogComment

from django.contrib import messages
from blog.templatetags import extras
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger



# Create your views here.

def blogHome(request):
    all_my_Posts = Post.objects.all()
    all_Posts = Paginator(all_my_Posts,2)
    
    page = request.GET.get('page')
    try:
        allPosts = all_Posts.page(page) 
    except PageNotAnInteger:
        allPosts = all_Posts.page(1)
    except EmptyPage:
        allPosts = all_Posts.page(all_Posts.num_page)


    #allPosts = Post.objects.all()
    #context = {'allPosts' : allPosts}
    context = {'allPosts' : allPosts}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    if post is not None:
        post.views = post.views + 1
        post.save()
    comments = BlogComment.objects.filter(post=post,parent =None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno  not  in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply) 

    print(replyDict)             

    #print(comments,replies)
    context = {'post': post ,'comments':comments,'user': request.user,'replyDict':replyDict}
    print(request.user)
    return render(request, 'blog/blogPost.html' ,context)


def postComment(request):
    if request.method=="POST":
        
        comment = request.POST.get("comment")
        user =  request.user
        postSno =  request.POST.get("postSno")
        post = Post.objects.get(sno = postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment =  BlogComment(comment =comment,user=user,post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")


        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment =  BlogComment(comment =comment,user=user,post=post,parent=parent)

            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    
    
    return redirect(f"/blog/{post.slug}")



