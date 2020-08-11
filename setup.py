import os
from setuptools import find_packages, setup

# with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
#     README = readme.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-blog-pkg',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',
    description='django-blog-pkg is a simple django blog app to help developers add simple blogs to their main projects. The app allows creating, updating and deleting of posts. It also allows comments on each post. Posts can be grouped under different Tags(categries).',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yemiemy/django-blog-pkg",
    author='Olaoluwayemi Rasheed',
    author_email = 'rasholayemi@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)