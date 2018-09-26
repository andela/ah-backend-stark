import jwt

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.template.defaultfilters import slugify
from authors.apps.authentication.models import User

class Article(models.Model):
    # Still Under Construction. Some of the fields and datatypes
    # May be for test purposes and for they alone

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,max_length=255)
    description = models.CharField(max_length=500)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)



    class Meta:
        ordering = ['created_on']


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Article,self).save(*args , **kwargs)

    def __str__(self):
        return self.title


