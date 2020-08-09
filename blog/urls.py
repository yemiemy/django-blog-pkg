from django.urls import path
from .views import (
    postDetailView, 
    TagPostListView, 
    PostListView, 
    search_view,
    AuthorPostListView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView)

urlpatterns = [
    path('blog/<int:pk>-<str:slug>/', postDetailView, name='post_detail'),
    path('', PostListView.as_view(), name='post_list'),
    path('search/', search_view, name='search_blog'),
    path('category/<str:name>', TagPostListView.as_view(), name='post_tag'),
    path('post/<str:username>', AuthorPostListView.as_view(), name='user_post'),
    path('post/<int:pk>-<str:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>-<str:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('create/new/', PostCreateView.as_view(), name='post_create'),
]