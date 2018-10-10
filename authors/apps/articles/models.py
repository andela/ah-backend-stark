import re
from django.db import models
from django.template.defaultfilters import slugify
from authors.apps.authentication.models import User
from ast import literal_eval
from django.utils import timezone


class Article(models.Model):
    """
    The Articles model class
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    description = models.CharField(max_length=500)
    body = models.TextField()
    tagList = models.CharField(max_length=2000, blank=True)
    image = models.URLField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    favorited = models.BooleanField(default=False)
    favoritesCount = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    ratingsCount = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['createdAt']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()

        super(Article, self).save(*args, **kwargs)

    def generate_slug(self):
        """
        This method generates a unique slug for every article by first
        checking for its existence
        """
        slug = slugify(self.title)
        current_slug_queryset = Article.objects.filter(
            slug__istartswith=slug)
        slug_count = current_slug_queryset.count()
        unique_slug = slug

        if slug_count:
            current_slug_queryset.order_by('slug')

            last_article = current_slug_queryset.last()
            last_slug_str = last_article.slug
            last_digits_regx = r"\d+$"
            slug_matches = re.search(last_digits_regx, last_slug_str)

            if slug_matches:
                last_digits = int(slug_matches.group())
                last_digits += 1
                unique_slug = slug + str(last_digits)
            else:
                unique_slug += "00"

        return unique_slug

    @staticmethod
    def title_exists(user_id, title):
        return Article.objects.filter(
            author=user_id, title__iexact=title).exists()

    def article_exists(slug):
        return Article.objects.filter(slug=slug).exists()

    @staticmethod
    def get_article(slug):
        return Article.objects.filter(slug=slug).first()

    @staticmethod
    def get_single_article(slug):
        return Article.objects.filter(slug=slug)

    @staticmethod
    def get_article_by_author(author_id, slug):
        return Article.objects.filter(
            author=author_id, slug=slug)

    @staticmethod
    def delete_article(author_id, slug):
        article = Article.objects.filter(
            author=author_id, slug=slug)
        statusCode = 200
        message = 'Article deleted successfully'

        if article:
            article.delete()
        else:
            if Article.article_exists(slug):
                statusCode = 403
                message = (
                    'You do not have rights to delete the selected article')
            else:
                statusCode = 404
                message = 'The selected article was not found'

        return (message, statusCode)

    @staticmethod
    def update_article(author_id, slug, new_data):
        article_queryset = Article.get_article_by_author(
            author_id, slug)
        article = article_queryset.first()

        statusCode = 202
        message = 'Article updated successfully'

        if article:

            new_title = new_data.get('title', article.title)
            # assign the new title to the current article to enable
            # slug generation
            article.title = new_title

            new_slug = article.generate_slug()
            new_description = new_data.get(
                'description', article.description)
            new_body = new_data.get('body', article.body)
            new_tagList = str(new_data.get('tagList', article.tagList))
            new_image = new_data.get('image', article.image)
            updated_time = timezone.now()

            article_queryset.update(
                       title=new_title,
                       slug=new_slug,
                       description=new_description,
                       body=new_body,
                       tagList=new_tagList,
                       image=new_image,
                       updatedAt=updated_time)

            article = Article.get_article(new_slug)
            # return the modified article instead of the default message
            message = article

        else:
            if Article.article_exists(slug):
                statusCode = 403
                message = (
                    'You do not have rights to edit the selected article')
            else:
                statusCode = 404
                message = 'The selected article was not found'

        return (message, statusCode)

    @staticmethod
    def format_data_for_display(data):

        # Format the tagList field and convert it back to list format
        formatted_data = data
        if isinstance(data, list):

            for count, record in enumerate(formatted_data):
                taglist = formatted_data[count]['tagList']
                if taglist:
                    formatted_data[count]['tagList'] = literal_eval(taglist)
                else:
                    formatted_data[count]['tagList'] = []

        else:
            if isinstance(data, dict):
                taglist = formatted_data.get('tagList', None)
                if taglist:
                    formatted_data['tagList'] = literal_eval(taglist)
                else:
                    formatted_data['tagList'] = []

        return formatted_data

    @staticmethod
    def calculate_rating(
            current_rating, current_rating_count, user_rating):
        """
        This method calculates the average rating considering the current
        average rating, the new user rating and the number of people who
        have rated it
        """
        numerator = (current_rating * current_rating_count) + user_rating
        current_rating_count += 1
        rating = numerator / current_rating_count
        return {"rating": rating, "ratingsCount": current_rating_count}

    def __str__(self):
        return self.title

    def likes(self):
        likes = Likes.objects.all().filter(
            article_id=self.id, action=True).count()
        return likes

    def dislikes(self):
        dislikes = Likes.objects.all().filter(
            article_id=self.id, action=False).count()
        return dislikes


class Likes(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    action_by = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.BooleanField()
    action_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return str(self.user.username)

    def __unicode__(self):
        return str(self.user.username)

    def children(self):
        return Comment.objects.filter(parent_comment=self)

    def is_parent(self):
        if self.parent_comment is not None:
            return False
        return True
