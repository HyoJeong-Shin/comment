from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Comment
from .forms import BlogForm, CommentForm
from django.contrib.auth.models import User
from django.contrib import auth


def home(request):
    blogs = Blog.objects
    return render(request, 'blog/home.html', {'blogs': blogs})


def create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BlogForm()
    return render(request, 'blog/create.html', {'form': form})


def detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        comment_form.instance.blog_id = pk
        if comment_form.is_valid():
            comment = comment_form.save()
    comment_form = CommentForm()
    comments = blog.comments.all()
    return render(request, 'blog/detail.html', {'blog': blog, 'comments': comments,'comment_form': comment_form})

def update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('/blog/'+str(blog.id))
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/update.html', {'form': form})


def delete(request, pk):
    blog = Blog.objects.get(pk=pk)
    blog.delete()
    return redirect('home')

#comment 기능 #
def comment_update(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    blog = get_object_or_404(Blog, pk=comment.blog.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('/blog/'+str(blog.id))
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_update.html', {'form': form})

def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    blog = get_object_or_404(Blog, pk=comment.blog.id)

    if request.method == 'POST':
        comment.delete()
        return redirect('/blog/'+str(blog.id))
    else:
        return render(request,'blog/comment_delete.html',{'object': comment})


def signup(request):
    if request.method == "POST":    # 요청방식이 POST방식인지 확인
        if request.POST['password1'] == request.POST['password2']:   # 입력한 비밀번호와 비밀번호 확인 부분이 같은지 확인
            user = User.objects.create_user(    # 유저 생성하는 함수
                request.POST['username'],   # 입력 받은 유저이름
                password = request.POST['password1']    # 입력 받은 패스워드
            )
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')   # 그 계정에 로그인을 하라는 요청을 다시 보냄
            return redirect('home')     # 메인으로 사용자가 갈 수 있게 리턴함
    return render(request, 'blog/signup.html')   # 요청 방식이 POST가 아니라면 회원가입 페이지에 머무름


def login(request):
    if request.method == 'POST':    # POST 방식으로 들어온 지 확인
        username = request.POST['username'] # 사용자로부터 전달 받은 유저 이름을 넣음
        password = request.POST['password'] # 사용자로부터 전달 받은 패스워드를 넣음
        user = auth.authenticate(request, username=username, password=password) # 전달받은 변수를 유저 변수에 넣어줌
        if user is not None:    # 유저가 존재한다면
            auth.login(request, user)   # 이 유저가 존재하므로 로그인 해줌 
            return redirect('home')     # 메인 페이지로 이동
        else:
            return render(request, 'blog/login.html')    # 존재하지 않으면 로그인 페이지에 남아있게됨
    else:        
        return render(request, 'blog/login.html')    # POST방식이 아닐 경우 로그인 페이지에 남아있게 됨


def logout(request):    #로그아웃에 대한 요청이 들어온다면, 
    if request.method == 'POST':
        auth.logout(request)    # auth.logout함수를 작동 => 로그아웃 진행됨
        return redirect('home') # 메인 페이지로 이동
    return render(request, 'signup.html')