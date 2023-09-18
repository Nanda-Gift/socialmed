from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import auth ,messages
from .models import profile,Post,likepost,followscount
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
# Create your views here.

@login_required(login_url='/signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile=profile.objects.get(user=user_object)
    

    user_following_list = []
    feed = []
    user_following = followscount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user =usernames)
        feed.append(feed_lists)    

    feed_list = list(chain(*feed))

    # suggestion for following
    all_users =User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
        
    new_suggestion_list =[x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestion_list =[x for x in list(new_suggestion_list) if (x not in list(current_user))]
    random.shuffle(final_suggestion_list)

    username_profile =[]
    username_profile_list =[]

    for users in final_suggestion_list:
        username_profile.append(users.id)
    for ids in username_profile:
        profile_lists = profile.objects.filter(userid=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_list =list(chain(*username_profile_list))

    return render(request, 'index.html',{'user_profile':user_profile,'post_views':feed_list,'suggestions_username_list':suggestions_username_list[:5]})


def signup(request):
    if request.method == 'POST':
        username =request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2=request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken')
                return redirect('signup')
            else:
                user= User.objects.create_user(username=username,email=email,password=password)
                user.save()

                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)



                user_model = User.objects.get(username=username)
                user_profile=profile.objects.create(user=user_model,userid=user_model.id)
                user_profile.save()
                return redirect('settings')


        else:
            messages.info(request,"password is not matching")
            return redirect('signup')




    else :   
        return render(request,'signup.html')
    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid input")
            return redirect('signin')
        
    else:
        return render(request,'signin.html')

@login_required(login_url='/signin')
def Logout(request):
    auth.logout(request)
    return redirect('signin')



@login_required(login_url='/signin')
def settings(request):
    user_profile = profile.objects.get(user=request.user)

    if request.method == "POST":
        if request.FILES.get('profileImg') == None:
            profileImg = user_profile.profileImg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileImg=profileImg
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()

        if request.FILES.get('profileImg') != None:
            profileImg=request.FILES.get('profileImg')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileImg=profileImg
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        return redirect('settings')  


    return render(request,'setting.html',{'user_profile':user_profile})

@login_required(login_url='/signin')
def upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST['caption']
        user = request.user.username
        post_user = Post.objects.create(user=user,caption=caption,image=image)
        post_user.save()
        messages.info(request,"file upload successful")
        return redirect('/')
        
    

    else:
        messages.info(request,'not upload')
        return redirect('/')
    
@login_required(login_url='/signin')
def likes(request):
    username= request.user.username
    post_id = request.GET.get('post_id')
    

    var_post = Post.objects.get(id=post_id)
    like_filter = likepost.objects.filter(post_id=post_id,username=username).first()

    if like_filter == None:
        new_like = likepost.objects.create(username=username,post_id=post_id)
        new_like.save()
        var_post.no_of_likes=var_post.no_of_likes+1
        var_post.save()
        return redirect('/')
    else:
        like_filter.delete()
        var_post.no_of_likes=var_post.no_of_likes-1
        var_post.save()
        return redirect('/')    
    
@login_required(login_url='/signin')
def profiles(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = profile.objects.get(user=user_object)
    user_post = Post.objects.filter(user=pk)
    user_post_length = len(user_post)
    follower = request.user.username
    user = pk
    if followscount.objects.filter(follower=follower,user=user).first():
        button_text = 'unfollow'
    else:
        button_text = 'follow'

    user_follower = len(followscount.objects.filter(user=pk))
    user_following = len(followscount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile':user_profile,
        'user_post':user_post,
        'user_post_length':user_post_length,
        'button_text':button_text,
        'user_follower': user_follower,
        'user_following': user_following,
    }

    return render(request,'profile.html',context)

@login_required(login_url='/signin')
def follows(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user= request.POST['user']

        if followscount.objects.filter(follower=follower,user=user).first():
            delete_follower=followscount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profiles/'+user)
        
        else:
            new_follower = followscount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profiles/'+user)
        
    else:
        return redirect('/')

def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = profile.objects.get(user =user_object)

    if request.method == "POST":
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile =[]
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = profile.objects.filter(userid=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))

    return render(request,'search.html',{'user_profile':user_profile,'username_profile_list':username_profile_list})