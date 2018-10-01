import jwt
import re
from rest_framework.views import exceptions

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.template.defaultfilters import slugify
from authors.apps.authentication.models import User
from ast import literal_eval

class Article(models.Model):
    """
    The Articles model class
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,max_length=255,blank=True)
    description = models.CharField(max_length=500)
    body = models.TextField()
    tagList = models.CharField(max_length=2000,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    favorited = models.BooleanField(default=False)
    favoritesCount = models.IntegerField(default=0)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    
    class Meta:
        ordering = ['createdAt']


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()

            super(Article,self).save(*args , **kwargs)

    def generate_slug(self):
        """
        This method generates a unique slug for every article by first
        checking for the existence of a given title
        """
        slug = slugify(self.title)
        current_slug_queryset = Article.objects.filter(slug__istartswith=slug)
        slug_count = current_slug_queryset.count()
        unique_slug = slug

        if slug_count:
            current_slug_queryset.order_by('slug')

            if Article.objects.filter(author=self.author,title__iexact=self.title).exists():
                # this author already has a title with the same name
                # return conflict error code

                # A wrong status code is being returned here. 
                # Still a work in progress
                raise exceptions.NotAcceptable('You already have an article with the same title')
                ##
                ##

            else:
                last_slug = current_slug_queryset.last()
                last_slug_str = last_slug.slug
                last_digits_regx = "\d+$"
                slug_matches = re.search(last_digits_regx, last_slug_str)

                if slug_matches:
                    last_digits = int(slug_matches.group())
                    last_digits+=1
                    unique_slug = slug + str(last_digits)

        return unique_slug

    @property
    def tags(self):
        """
        This will leverage python's ast module to convert the tagList field
        back to its original python datatype i.e, list

        """
        tag_list = literal_eval(self.tagList)
        
        if isinstance(tag_list,str):
            tag_list = [] # No tags were specified for the article. Just return an empty list
        return tag_list


    def __str__(self):
        return self.title


