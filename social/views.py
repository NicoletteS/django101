from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseForbidden
from django.core.urlresolvers import reverse
from social.models import Post, Comment, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from social.models import Comment, Post # put this at the top with the other imports

# Create your views here.

def index(request):
    return render(request, 'social/index.html')
    
def social_login(request):
   check = _check_post_request(request, ['username', 'password'])
   if check[0]:
       user = authenticate(username=request.POST['username'], password=request.POST['password']) 
       if user is not None:
           login(request, user)
           return HttpResponseRedirect(reverse('social:home'))
       else:
           return HttpResponseBadRequest("The combination of username and password does not exist.")
   else:
       return HttpResponseBadRequest(check[1])

@login_required
def home(request):
    if request.method == 'GET':
        posts = Post.objects.all()
    elif request.method == 'POST':
        check = _check_post_request(request, ['search_terms'])
        if check[0]:
            search_term = request.POST['search_terms']
            posts = Post.objects.filter(text__icontains=search_term)
        else:
            return HttpResponseBadRequest(check[1])
    posts = posts.order_by('-date_time')
    return render(request, 'social/home.html', {'posts': posts, 'user': request.user})

def add_user(request):
    check = _check_post_request(request, ['username', 'password'])
    errorMsg = ""
    if check[0]:
        if User.objects.filter(username = request.POST['username']).exists():
            errorMsg = "This username is already in use!"
            return render(request, 'social/sign_up.html', {'error': errorMsg})
        try:
            validate_password(request.POST['password'])
        except ValidationError as error:
            errorMsg = str(error)    
            return render(request, 'social/sign_up.html', {'error': errorMsg})
        #new_user = User()
        #new_user.username = request.POST['username']
        #new_user.password = request.POST['password']
        new_user = User.objects.create_user(request.POST['username'], '', request.POST['password'])
        new_user.save()
        return render(request, 'social/index.html')    
    else:
        return HttpResponseBadRequest(check[1])

def sign_up(request):
    return render(request, 'social/sign_up.html')

@login_required
def add_post(request):
    check = _check_post_request(request, ['text'])
    if check[0]:
        new_post = Post()
        new_post.text = request.POST['text']
        new_post.poster = request.user
        if 'photo' in request.FILES and request.FILES['photo'] is not None:
            new_post.photo = request.FILES['photo']
        new_post.save()
        #save_to_csv(request)
        return HttpResponseRedirect(reverse('social:home'))
    else:
        return HttpResponseBadRequest(check[1])

def _check_post_request(request, keys):
    if request.method != 'POST':
        return (False, "This method should be called with a POST method!")
    for key in keys:
        if key not in request.POST:
            return (False, "The POST request should contain a {} field".format(key))
        if not request.POST[key]:
            return (False, "The {} field cannot be empty!".format(key))
    return (True, "Everything is alright!")
        
def _check_post_request(request, keys):
    # Check that the request method is POST
    if request.method != 'POST':
        return (False, "This method should be called with a POST method!")
    for key in keys:
        # Check that the key exists
        if key not in request.POST:
            return (False, "The POST request should contain a {} field".format(key))
        # Check that the text is not empty
        if not request.POST[key]:
            return (False, "The {} field cannot be empty!".format(key))

    return (True, "Everything is alright!")
	
def bubble(request):
	return render(request, 'social/bubble.html')

def bubble2(request):
    return render(request, 'social/bubble2.html')
    
@login_required
def add_comment(request):
    check = _check_post_request(request, ['comment', 'post_id'])
    if check[0]:
        new_comment = Comment()
        new_comment.poster = request.user 
        new_comment.text = request.POST['comment']
        try:
            post = Post.objects.get(pk=request.POST['post_id'])
            new_comment.post = post
        except Post.DoesNotExist:
            return HttpResponseBadRequest("There is no Post with id {}".format(request.POST['post_id']))
        new_comment.save()
        return HttpResponseRedirect(reverse('social:home'))
    else:
        return HttpResponseBadRequest(check[1])
        
@login_required
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user != post.poster:
        return HttpResponseForbidden("You can only delete your own posts!")
    else:
        post.delete()
        return HttpResponseRedirect(reverse('social:home'))