from django.db import models
from django.conf import settings 
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Tag(models.Model):
    """ Tag class for creating different tags(categories) for posts.
	
		Attributes:
			name (str) representing the name of the tag.
        Relationship:
            Tag has a one to many(posts) relationship with Post class.
        The `urlpatterns` info:
        `path('category/<str:name>', TagPostListView.as_view(), name='post_tag')`
        
	"""
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    """Post class for writing blog content.

    Attributes:
    ```
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
    ```
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    tag = models.ForeignKey(Tag, null=True, blank=True, on_delete=models.CASCADE)
    body = RichTextUploadingField()
    image = models.ImageField(upload_to='blog/', null=True, blank=True)
    credit = models.CharField(max_length=120, null=True, blank=True)
    featured = models.BooleanField(default=False)
    published = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(
        default='',
        editable=False,
        max_length=120,
    )

    def __str__(self):
        return f'{self.title} on {self.published}'
        

    class Meta:
        unique_together = ('title', 'slug')

    def get_absolute_url(self):
        kwargs = {
            'pk': self.id,
            'slug': self.slug
        }
        return reverse('post_detail', kwargs=kwargs)

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

class Comment(models.Model):
    """Comment class for taking in comments per post.
    Attributes:
    ```
        1. post (FoereignKey to Post model) This field has a relationship of many to one(post).
        2. writer (CharField) This takes in the name of the writer.
        3. email (EmailField) This takes in the email of the writer. 
        4. website (CharField) This takes in the website of the writer (optional).
        5. body (TextField) This is the main message by the writer.
        6. active (bool) If set to True, comment is diplayed in the post-detail page. default = True
        7. published (DateTimeField) This takes in the date and time for the comment creation. It auto fills.
        8. def __str__(self) -- This returns name of the writer and published date.
    ```
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    writer = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=120)
    website = models.CharField(max_length=120, blank=True, null=True)
    body = models.TextField()
    active = models.BooleanField(default=True)
    published = models.DateTimeField(auto_now_add=True)
    def __str__(self):

        return "{} commented on {}".format(self.writer,self.published.date())

