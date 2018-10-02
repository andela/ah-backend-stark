from rest_framework import status
from authors.apps.articles.tests import BaseTest

class TestArticle(BaseTest):
    """
    This class runs tests on the articles API endpoints
    """

    def test_article_creation(self):
        self.register_user(self.sample_user) # First register a user

        response = self.client.post('/api/articles/',self.article_1,format="json")
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIn('Titlely',response.data['title'])
        self.assertIn('This is my article',response.data['body'])

    def test_get_all_articles(self):
        pass

    def test_get_single_article(self):
        pass

        

