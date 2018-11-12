"""base test file"""

from django.test import TestCase
from rest_framework.test import APIClient
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article, Comment


class BaseTest(TestCase):
    """authentication app basetest class"""

    def setUp(self):
        """test class set up method"""

        self.client = APIClient()
        self.reg_data = {
            "user": {
                "username": "test12",
                "email": "test@test.com",
                "password": "Testpassword1"
            }
        }

        self.deactive_user = {
            "user": {
                "username": "test6",
                "email": "test6@test.com",
                "is_active": "False",
                "password": "testpassword"
            }
        }
        self.reg_data2 = {
            "user": {
                "username": "test7",
                "email": "test7@test.com",
                "password": "Testpassword2"
            }
        }

        self.login_data = {
            "user": {
                "email": "test@test.com",
                "password": "Testpassword1"
            }
        }

        self.login_data2 = {
            "user": {
                "email": "test7@test.com",
                "password": "Testpassword2"
            }
        }

        self.missing_username = {
            "user": {
                "username": "",
            }
        }

        self.short_username = {
            "user": {
                "username": "test",
                "email": "test6@test.com",
                "password": "12345678"
            }
        }

        self.missing_email = {
            "user": {
                "username": "test12",
                "email": "",
                "password": "test_password"
            }
        }

        self.invalid_email = {
            "user": {
                "username": "test12",
                "email": "test",
                "password": "test_password"
            }
        }

        self.short_password = {
            "user": {
                "username": "test12",
                "email": "test@test.com",
                "password": "test"
            }
        }

        self.password_with_no_caps = {
            "user": {
                "username": "test12",
                "email": "test@test.com",
                "password": "testpassword1"
            }
        }

        self.missing_password = {
            "user": {
                "username": "test12",
                "email": "test@test.com",
                "password": ""
            }
        }

        self.pswd_no_number = {
            "user": {
                "username": "test12",
                "email": "test@test.com",
                "password": "Testpassword"
            }
        }

        self.profile_update = {
            "profile": {
                "username": "test1",
                "email": "test6@test.com",
                "bio": "test",
                "location": "mbuya"
            }
        }

        self.password_update = {"user": {"password": "Newpaswd1"}}
        User.objects.create_user(
            "test5", "test5@test.com", password="Testpassword3")
        self.user = User.objects.get(email="test5@test.com")
        self.user.is_active = True
        self.user.save()

        self.article_1 = {
            "article": {
                "title": "Titlely",
                "description": "Now, how do you describe this?",
                "body": "This is my article",
                "tagList": ["Health", "Safety"]
            }
        }

        self.article_2 = {
            "article": {
                "title": "let me see",
                "description": "Describe?",
                "body": "La body",
                "tagList": ["Hello", "Hmm"]
            }
        }

        self.article_3 = {
            "article": {
                "title": "title 3",
                "description": "description 4?",
                "body": "body",
                "tagList": ["medium", "bold"]
            }
        }

        self.article_4 = {
            "article": {
                "title": "my story",
                "description": "Describe?",
                "body": "La body",
                "tagList": ["Hello", "Hmm"]
            }
        }

        self.invalid_article = {
            "article": {
                "title": "title me",
            }
        }

        self.modified_article = {
            "article": {
                "title": "Modified title",
                "description": "The description is also different"
            }
        }
        self.like_article = {"like": {"action": 1}}
        self.dislike_article = {"like": {"action": 0}}

        self.user_email = {"user": {"email": "test@test.com"}}

        self.article_rating_4 = {"article": {"rating": 4}}

        self.article_rating_5 = {"article": {"rating": 5}}

        self.article_rating_6 = {"article": {"rating": 6}}
        self.like_article = {"like": {"action": 1}}
        self.dislike_article = {"like": {"action": 0}}

        self.user_email = {"user": {"email": "test@test.com"}}

        self.comment1 = {"comment": {"body": "something else"}}
        # Test the article model functions
        self.article = Article.objects.create(
            title="lego",
            description='my description',
            body='my body',
            author=self.user)
        self.article.save()
        # update the article
        Article.update_article(self.user.id, 'lego', self.article_2)
        # check whether the modified article exists via new slug
        Article.article_exists('let-me-see')
        test_data = Article.get_article('let-me-see')
        # format data dict to be returned to the user
        Article.format_data_for_display(test_data)
        # get article by the user_id and slug
        Article.get_article_by_author(self.user.id, 'let-me-see')
        # delete an article
        Article.delete_article(self.user.id, 'let-me-see')

    def mock_login(self):
        """
        This helper method creates a user, logs then in,
        gets their token and sets the 'Token' header to the
        token generated during login

        It helps in authenticating requests
        """
        res = self.client.post("/api/users/", self.reg_data, format="json")
        token = res.data['token']
        self.client.get("/api/users/activate_account/{}/".format(token))
        login_response = self.client.post(
            "/api/users/login/", self.login_data, format="json")

        data = login_response.data
        token = data['token']
        self.client.credentials(HTTP_TOKEN=token)

    def different_user_mock_login(self):
        """
        This helper method creates a user, logs then in,
        gets their token and sets the 'Token' header to the
        token generated during login

        It helps in authenticating requests
        """
        res = self.client.post("/api/users/", self.reg_data2, format="json")
        token = res.data['token']
        self.client.get("/api/users/activate_account/{}/".format(token))
        login_response = self.client.post(
            "/api/users/login/", self.login_data2, format="json")

        data = login_response.data
        token = data['token']
        self.client.credentials(HTTP_TOKEN=token)

        self.comment = Comment.objects.create(
            user=self.user,
            body="how about we try something new.",
            article=self.article)
        self.comment.save()
        self.client.post(
            '/api/articles/titlely/comments/',
            data=self.comment1,
            format="json")

    def create_article(self, article):
        self.client.post('/api/articles/', article, format="json")
