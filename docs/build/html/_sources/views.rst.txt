Views
=====

PostListView(ListView)
----------------------

PostListView class lists all the posts objects. ::
    
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
    
    The 'urlpatterns' info: ::

        path('', PostListView.as_view(), name='post_list')

TagPostListView(ListView)
-------------------------

TagPostListView lists all the posts under a particular tag. ::
    
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

    The `urlpatterns` info: ::
    
        path('category/<str:name>', TagPostListView.as_view(), name='post_tag')
        
AuthorPostListView(ListView)
----------------------------

AuthorPostListView lists all the posts by a particular user(author). ::
    
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

    The `urlpatterns` info: ::

        path('post/<str:username>', AuthorPostListView.as_view(), name='user_post')

PostCreateView(LoginRequiredMixin, CreateView)
----------------------------------------------

PostCreateView creates a new post.
    NOTE: user has to be authenticated to create a post. ::

        1. model = Post
        2. fields = ['title', 'image', 'body', 'tag']

    The `urlpatterns` info: ::

        path('create/new/', PostCreateView.as_view(), name='post_create')

PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView)
-------------------------------------------------------------------

PostUpdateView updates an existing post.
        NOTE: 
            1. user must be authenticated to delete a post. 
            2. user must be author of a post to delete that post. ::
   
                model = Post
                fields = ['title', 'image', 'body', 'tag']
   
    The `urlpatterns` info: ::
        
        path('post/<int:pk>-<str:slug>/update/', PostUpdateView.as_view(), name='post_update')

PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView)
-------------------------------------------------------------------

PostDeleteView deletes an existing post. 
        NOTE: 
            1. user must be authenticated to delete a post. 
            2. user must be author of a post to delete that post. ::
    
                model = Post
                success_url = '/blog'

    The `urlpatterns` info: ::

        path('post/<int:pk>-<str:slug>/delete/', PostDeleteView.as_view(), name='post_delete')


postDetailView(request, pk, slug)
---------------------------------

postDetailView displays the details of a post.

        Args:
            1. pk (int) This is the unique primary key(id number) of each post.
            2. slug (slug) This is the unique slug auto generated from the title of each post.

        It checks for request method. if request method is `POST`, it takes in the required field 
        to create a comment object related to the particular post.

        It displays all the comment associated with a post on the detail page of that post.
    
    The `urlpatterns` info: ::

        path('blog/<int:pk>-<str:slug>/', postDetailView, name='post_detail')

search_view(request)
--------------------

search_view searches through the Post objects.

        It uses the `GET` request to take in the `query` and searches through the 
        `Post title` and `Post body`.
    
    The `urlpatterns` info: ::

        path('search/', search_view, name='search_blog')