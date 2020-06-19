from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact

from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def home(request):
    return render(request, 'home/home.html')
    # return HttpResponse("This is home")

def about(request):
    return render(request, 'home/about.html')
    # return HttpResponse("This is about")



def contact(request):
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email'] 
        phone = request.POST['phone'] 
        content = request.POST['content']
        print(name,email,phone,content)
        

        if len(name)<2 or len(email)< 3 or len(phone)< 10 or len(content)< 4:
            messages.error(request,"Please fill the form corrrectly")
        else:    
            contact = Contact(name=name,phone=phone,email=email,content=content)
            contact.save()
            messages.success(request,"Your messages has been successfully sent")
        
    return render(request, 'home/contact.html')
    # return HttpResponse("This is contact")

def search(request):
    query = request.GET['query']
    if len(query)>100:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request,"Please go for the right Keyword")    
    params = {'allPosts': allPosts,'query':query}
    return render(request,'home/search.html', params)


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # check for errornous inputs
        if len(username)>10:
            messages.error(request,"Your Username must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request,"Username must contain letters and numbers characters")
            return redirect('home')
        if pass1 != pass2 :
            messages.error(request,"Password not matched") 
            return redirect('home')       



        #create the user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your Account Has Been Successfully Created")
        return redirect('home')

    else:
        return HttpResponse('404 Not Found')    



def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user  = authenticate(username=loginusername,password= loginpassword)
     

        if user is not None:
            login(request,user)
            messages.success(request,'Successfully Logged In')
            return redirect('home')
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('home')   

    return HttpResponse('404 Not Found')

    

def handleLogout(request):
    logout(request)
    messages.success(request,'Successfully Logged Out')
    return redirect('home')

    

       