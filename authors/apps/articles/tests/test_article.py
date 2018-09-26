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

    def test_creation_of_invalid_article(self):
        self.mock_login()
        response = self.client.post('/api/articles/', self.invalid_article, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_getting_innexistent_article(self):
        response = self.client.get('/api/articles/brave-new-world-556')
        self.assertEqual(response.status_code,404)
        

    def test_duplication_of_title_by_same_user(self):
        self.mock_login()
        self.client.post('/api/articles/',self.article_1,format="json")
        response = self.client.post('/api/articles/',self.article_1,format="json")
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertIn(response.data.get('errors')[0],
        "You already have an article with the same title")

    def test_creation_of_existing_title_by_different_user(self):
        self.different_user_mock_login()
        response = self.client.post('/api/articles/',self.article_1,format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Titlely', response.data['title'])

    def test_deletion_of_article_by_owner(self):
        self.mock_login()
        self.client.post('/api/articles/',self.article_1,format="json")
        response = self.client.delete('/api/articles/titlely')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data.get('message'),"Article deleted successfully")

    def test_deletion_of_article_by_non_owner(self):
        self.mock_login()
        self.client.post('/api/articles/',self.article_1,format="json")
        self.different_user_mock_login()
        response = self.client.delete('/api/articles/titlely')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        self.assertIn('You do not have rights to delete',response.data.get('message'))


    def test_update_of_article_by_owner(self):
        self.mock_login()
        self.client.post('/api/articles/', self.article_1, format="json")
        edit_response = self.client.put('/api/articles/titlely', self.modified_article,format="json")
        get_response = self.client.get('/api/articles/modified-title')
        data = get_response.data.get('article')

        self.assertEqual(edit_response.status_code,status.HTTP_202_ACCEPTED)
        self.assertEqual(get_response.status_code,status.HTTP_200_OK)
        self.assertEqual(data.get('title'),"Modified title")
        self.assertEqual(data.get('description'),"The description is also different")



        

