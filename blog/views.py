from django.shortcuts import render, get_object_or_404, redirect, Http404, redirect
from datetime import datetime
from .models import Post, Comment, Tag
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


class PostListView(ListView):
    """PostListView class lists all the posts objects.
    ```
        1. model = Post
        2. context_object_name = 'posts'
        3. template_name = 'blog/post_list.html'
        4. ordering = ['-id']
        5. paginate_by = 4
        def get_context_data(self, **kwargs):
            return the following contexts: 
                'objects': Post.objects.all().order_by('-published')[:5],
                'year':datetime.now().year,
                'tags': Tag.objects.all() 
    ```
    The `urlpatterns` info:
    `path('', PostListView.as_view(), name='post_list')`
        
    """
    model = Post
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 4
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'objects': Post.objects.all().order_by('-published')[:5],
            'year':datetime.now().year,
            'tags': Tag.objects.all() 
        })  
        return context
    

class TagPostListView(ListView):
    """TagPostListView lists all the posts under a particular tag.
    
    ```
        1. model = Post
        2. context_object_name = 'posts'
        3. template_name = 'blog/post_list.html'
        4. ordering = ['-id']
        5. paginate_by = 4
        def get_context_data(self, **kwargs):
            return the following contexts: 
                'objects': Post.objects.all().order_by('-published')[:5],
                'year':datetime.now().year,
                'tags': Tag.objects.all() 
    ```
    The `urlpatterns` info:
    `path('category/<str:name>', TagPostListView.as_view(), name='post_tag')`
        
    """
    model = Post
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'objects': Post.objects.all().order_by('-published')[:5],
            'year':datetime.now().year,
            'tags': Tag.objects.all() 
        })  
        return context

    def get_queryset(self):
        tag = get_object_or_404(Tag, name=self.kwargs.get('name'))
        return Post.objects.filter(tag=tag).order_by('-id')


class AuthorPostListView(ListView):
    """AuthorPostListView lists all the posts by a particular user(author).
    
    ```
        1. model = Post
        2. context_object_name = 'posts'
        3. template_name = 'blog/post_list.html'
        4. ordering = ['-published']
        5. paginate_by = 4
        def get_context_data(self, **kwargs):
            return the following contexts: 
                'objects': Post.objects.all().order_by('-published')[:5],
                'year':datetime.now().year,
                'tags': Tag.objects.all() 
    ```
    The `urlpatterns` info:
    `path('post/<str:username>', AuthorPostListView.as_view(), name='user_post')`
        
    """
    model = Post
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'objects': Post.objects.all().order_by('-published')[:5],
            'tags': Tag.objects.all()  
        })  
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-published')

class PostCreateView(LoginRequiredMixin, CreateView):
    """PostCreateView creates a new post.
    NOTE: user has to be authenticated to create a post.
    ```
        1. model = Post
        2. fields = ['title', 'image', 'body', 'tag']
    ``` 
    The `urlpatterns` info:
    `path('create/new/', PostCreateView.as_view(), name='post_create')`
      
    """
    model = Post
    fields = ['title', 'image', 'body', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'tags': Tag.objects.all().order_by('-id')
        })  
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """PostUpdateView updates an existing post.
        NOTE: 
            1. user must be authenticated to delete a post. 
            2. user must be author of a post to delete that post.
    ```
        model = Post
        fields = ['title', 'image', 'body', 'tag']
    ```
    The `urlpatterns` info:
    `path('post/<int:pk>-<str:slug>/update/', PostUpdateView.as_view(), name='post_update')`
    """
    model = Post
    fields = ['title', 'image', 'body', 'tag']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user': self.request.user.post_set.get(slug=self.kwargs.get('slug')),
            'tags': Tag.objects.all().order_by('-id')
        })  
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """PostDeleteView deletes an existing post. 
        NOTE: 
            1. user must be authenticated to delete a post. 
            2. user must be author of a post to delete that post.
    ```
    model = Post
    success_url = '/blog'
    ```
    The `urlpatterns` info:
    `path('post/<int:pk>-<str:slug>/delete/', PostDeleteView.as_view(), name='post_delete')`
    """
    model = Post
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def postDetailView(request, pk, slug):
    """postDetailView displays the details of a post.

        Args:
            1. pk (int) This is the unique primary key(id number) of each post.
            2. slug (slug) This is the unique slug auto generated from the title of each post.
        It checks for request method. if request method is `POST`, it takes in the required field 
        to create a comment object related to the particular post.

        It displays all the comment associated with a post on the detail page of that post.
    
    The `urlpatterns` info:
    `path('blog/<int:pk>-<str:slug>/', postDetailView, name='post_detail')`
    
    """
    try:
        post = get_object_or_404(Post, slug=slug)
        try:
            prev_post = Post.objects.get(id=post.id-1)
        except:
            prev_post = None
        try:
            next_post = Post.objects.get(id=post.id+1)
        except:
            next_post = None
        posts = Post.objects.all().order_by('-id')[:5]
        comments = post.comments.all().order_by('-id')
        count = 0
        for com in comments:
            if com.active:
                count+=1
        if request.method == 'POST':
            writer = request.POST['name']
            email = request.POST['email']
            website = request.POST['web']
            body = request.POST['body']

            comment = Comment.objects.create(
                post=post,
                writer=writer,
                email=email,
                website=website,
                body=body,
                published = datetime.now()
                )
            comment.save()
            return redirect('post_detail', pk, slug)
        return render(request, 'blog/post-detail.html', {
        'object':post,
        'objects':posts,
        'comments':comments,
        'tags': Tag.objects.all(), 
        'count':count,
        'prev_post':prev_post,
        'next_post':next_post})
    except Exception as e:
        return render(request, 'blog/error.html', {'e':e})
    


def search_view(request):
    """search_view searches through the Post objects.

        It uses the `GET` request to take in the `query` and searches through the 
        `Post title` and `Post body`.
    
    The `urlpatterns` info:
    `path('search/', search_view, name='search_blog')` 
    """
    query = request.GET['query']
    posts = Post.objects.filter(title__icontains=query)|Post.objects.filter(body__icontains=query)
	
    context = {
        'posts':posts.order_by('-id'),
        'query':query,
        'objects':Post.objects.all().order_by('-id')[:5],
        'tags': Tag.objects.all(), 
        'year':datetime.now().year
    }
    return render(request, 'blog/search.html', context)
