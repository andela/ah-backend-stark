import re
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
        checking for its existence
        """
        slug = slugify(self.title)
        current_slug_queryset = Article.objects.filter(slug__istartswith=slug)
        slug_count = current_slug_queryset.count()
        unique_slug = slug

        if slug_count:
            current_slug_queryset.order_by('slug')

            last_article = current_slug_queryset.last()
            last_slug_str = last_article.slug
            last_digits_regx = "\d+$"
            slug_matches = re.search(last_digits_regx, last_slug_str)

            if slug_matches:
                last_digits = int(slug_matches.group())
                last_digits += 1
                unique_slug = slug + str(last_digits)
            else:
                unique_slug += "00"

        return unique_slug

    @staticmethod
    def title_exists(user_id,title):
        return Article.objects.filter(author=user_id,title__iexact=title).exists()


    @staticmethod
    def get_single_article(slug):
        return Article.objects.filter(slug=slug)

    @staticmethod
    def format_data_for_display(data):

        # Format the tagList field and convert it back to list format
        formatted_data = data
        if isinstance(data,list):

           for count,record in enumerate(formatted_data):
               taglist = formatted_data[count]['tagList']
               if taglist:
                   formatted_data[count]['tagList'] = literal_eval(taglist)
               else:
                   formatted_data[count]['tagList'] = []

        else:
            if isinstance(data, dict):
                taglist = formatted_data.get('tagList',None)
                if taglist:
                    formatted_data['tagList'] = literal_eval(taglist)
                else:
                    formatted_data['tagList'] = []

        return formatted_data


    def __str__(self):
        return self.title


