=====
Blog App
=====
django-blog-pkg is a simple django blog app to help developers add simple blogs to their main projects. The app allows creating, updating and deleting of posts. It also allows comments on each post. Posts can be grouped under different Tags(categries).

Detailed documentation is found in the "README.md".

Installation
------------
1. Python Package
```
pip install django-blog-pkg
```

2. Other Important apps to DOWNLOAD:
```
pip install django-crispy-forms

pip install django-ckeditor

```

3. settings.py (Important - Please note 'django.contrib.humanize' is required as INSTALLED_APPS):
```
# Include the following in your INSTALLED_APPS

INSTALLED_APPS = [
    ...
    # The following apps are required:

    'django.contrib.humanize',
    'ckeditor',
    'crispy_forms',

    'blog',
    
]
# add the following directly below the INSTALLED_APPS

CKEDITOR_UPLOAD_PATH = 'uploads/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

```
4. urls.py 
```
urlpatterns = [
    ...
    path('blog/', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    ...
]
# You can use the URLs provided by blog: `post_list`, `post_detail`, `post_tag`, `post_update`, `post_delete`, `post_create`, `search_blog`, `user_post`

# now add the following lines of code

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


```

Post Installation 
-----------------
In your Django root execute the command below to create your database tables:
```
python manage.py makemigrations

python manage.py migrate
```
Start the development server 
---------------------------
`python manage.py runserver`

and visit `http://127.0.0.1:8000/admin/` or `http://127.0.0.1:8000/blog/create/new/`
to create blog posts (you'll need the Admin app enabled).


Source code
-----------

[django-blog-pkg](https://www.github.com/yemiemy/django-blog-pkg)