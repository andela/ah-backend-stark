from rest_framework import status
from authors.apps.authentication.tests import BaseTest

class TestArticle(BaseTest):
    """
    This class runs tests on the articles API endpoints
    """

    def test_article_creation(self):
        self.mock_login() # First register and login a user

        response = self.client.post('/api/articles/', self.article_1, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Titlely', response.data['title'])
        self.assertIn('This is my article', response.data['body'])

    def test_get_all_articles(self):
        response = self.client.get('/api/articles/')
        data = response.data
        self.assertEqual(response.status_code,200)
        self.assertTrue('articles' in data)
        self.assertIsInstance(data.get('articles'),list)


    def test_get_single_article(self):
        self.mock_login()
        self.client.post('/api/articles/',self.article_1,format="json")
        response = self.client.get('/api/articles/titlely')
        data = response.data
        self.assertEqual(response.status_code,200)
        self.assertTrue('article' in data)

    def test_duplication_of_title_by_same_user(self):
        self.mock_login()
        self.client.post('/api/articles/',self.article_1,format="json")
        response = self.client.post('/api/articles/',self.article_1,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn(response.data.get('errors')[0],
        "You already have an article with the same title")
        
