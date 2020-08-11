Models
======

Tag
---
Tag class for creating different tags(categories) for posts.
	
		Attributes:
			name (str) representing the name of the tag.
            
        Relationship:
            Tag has a one to many(posts) relationship with Post class.

        The `urlpatterns` info: ::

            path('category/<str:name>', TagPostListView.as_view(), name='post_tag')

Post
----

Post class for writing blog content.

    Attributes: ::
    
		1. author (ForeignKey to User model) representing the user that creates the post.
        2. title (CharField) representing the title of the post.
        3. tag (ForeignKey to Tag model) represents a many to one relationship with the Tag class.
        4. body (text) This is the body of the post. It uses CKEDITOR for advanced text editing (WYSIWYG).
        5. image (ImageField) This takes in the image of the post. It uploads to path `media/blog/`
        6. credit (CharField) This takes in the link to credits for images that require credits. (optional)
        7. featured (bool) If set to `True`, the post become featured and can be displayed on the home page. default = False
            Example:
                featured_posts = Post.objects.filter(featured=True)
        8. published (DateTimeField) This takes in the date and time for post creation. It auto fills.
        9. is_active (bool) If set to `True`, post can be made visible. defaukt = False
            Example:
                `active_posts = Post.objects.filter(is_active=True)` 
        10. slug (SlugField) this automatically generates slugs based on the title of the post.
            Example:
                `new-post`
        11. def __str__(self) -- This returns title of the posts and published dates
        12. get_absolute_url(self) -- This returns the absolute url of a post in the format `/blog/1-new-post/`
    
Comment
-------

Comment class for taking in comments per post.
    Attributes: ::
   
        1. post (FoereignKey to Post model) This field has a relationship of many to one(post).
        2. writer (CharField) This takes in the name of the writer.
        3. email (EmailField) This takes in the email of the writer. 
        4. website (CharField) This takes in the website of the writer (optional).
        5. body (TextField) This is the main message by the writer.
        6. active (bool) If set to True, comment is diplayed in the post-detail page. default = True
        7. published (DateTimeField) This takes in the date and time for the comment creation. It auto fills.
        8. def __str__(self) -- This returns name of the writer and published date.
        