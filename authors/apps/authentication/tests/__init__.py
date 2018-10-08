"""base test file"""

from django.test import TestCase
from rest_framework.test import APIClient
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article
class BaseTest(TestCase):
    """authentication app basetest class"""

    def setUp(self):
        """test class set up method"""

        self.client = APIClient()
        self.reg_data = {"user": {
            "username":"test",
            "email":"test@test.com",
            "password":"testpassword"
                }
                         }
        self.deactive_user = {"user": {
            "username":"test6",
            "email":"test6@test.com",
            "is_active":"False",
            "password":"testpassword"
                }
                              }
        self.reg_data2 = {"user": {
            "username":"test7",
            "email":"test7@test.com",
            "password":"testpassword"
                }
                          }
       
        self.login_data = {"user": {
            "email":"test@test.com",
            "password":"testpassword"}
                           }

        self.login_data2 = {"user": {
            "email":"test7@test.com",
            "password":"testpassword"}
                           }

        self.deactive_login = {"user": {
            "email":"test6@test.com",
            "password":"12345678"}
                               }

        self.missing_username = {
            "user": {
                "username":"",
                "email":"test@test.com",
                "password":"test_password"}
                                }

        self.missing_email = {
            "user": {
                "username":"test",
                "email":"",
                "password":"test_password"}
                            }

        self.invalid_email = {
            "user": {
                "username":"test",
                "email":"test",
                "password":"test_password"}
        }

        self.short_password = {
            "user": {
                "username":"test",
                "email":"test@test.com",
                "password":"test"}
                            }

        self.non_alphanumeric_password = {
            "user": {
                "username":"test",
                "email":"test@test.com",
                "password":"@$* p#$%"}
        }
        self.profile_update = {"profile": {
            "username":"test1",
            "email":"test6@test.com",
            "bio":"test",
            "location":"mbuya"}
                            }
        User.objects.create_user("test5", "test5@test.com", password="12345678")
        self.user = User.objects.get(email="test5@test.com")
        self.user.is_active = True
        self.user.save()

        register_user2 = self.client.post("/api/users/", self.deactive_user, format="json")
        token1 = register_user2.data["token"]
        self.client.credentials(HTTP_TOKEN=token1)

        self.article_1 = {"article": {
            "title": "Titlely",
            "description": "Now, how do you describe this?",
            "body": "This is my article",
            "tagList":["Health","Safety"]
               } 
        }

        self.article_2 = {"article": {
            "title": "let me see",
            "description": "Describe?",
            "body": "La body",
            "tagList":["Hello","Hmm"]
               } 
        }

        self.invalid_article = {"article": {
            "title": "title me",
               } 
        }

        self.modified_article = {"article": {
            "title": "Modified title",
            "description": "The description is also different"
               } 
        }

        self.article_rating_4 = {"article": {
            "rating": 4
                }
        }

        self.article_rating_5 = {"article": {
            "rating": 5
                }
        }

        self.article_rating_6 = {"article": {
            "rating": 6
                }
        }

        # Test the article model functions
        self.article = Article.objects.create(title="my title",
                                                description = 'my description',
                                                body='my body',author=self.user)
        self.article.save()
        # update the article
        Article.update_article(self.user.id,'my-title',self.article_2)
        # check whether the modified article exists via new slug
        Article.article_exists('let-me-see')
        test_data = Article.get_article('let-me-see')
        # format data dict to be returned to the user
        Article.format_data_for_display(test_data)
        # get article by the user_id and slug
        Article.get_article_by_author(self.user.id,'let-me-see')
        # delete an article
        Article.delete_article(self.user.id,'let-me-see')

    def mock_login(self):
        """
        This helper method creates a user, logs then in,
        gets their token and sets the 'Token' header to the
        token generated during login

        It helps in authenticating requests
        """
        self.client.post("/api/users/", self.reg_data, format="json")
        login_response = self.client.post("/api/users/login/",
                         self.login_data, format="json")

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
        self.client.post("/api/users/", self.reg_data2, format="json")
        login_response = self.client.post("/api/users/login/",
                         self.login_data2, format="json")

        data = login_response.data
        token = data['token']
        self.client.credentials(HTTP_TOKEN=token)      
