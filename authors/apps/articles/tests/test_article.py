from rest_framework import status
from authors.apps.authentication.tests import BaseTest


class TestArticle(BaseTest):
    """
    This class runs tests on the articles API endpoints
    """

    def test_article_creation(self):
        self.mock_login()
        response = self.client.post(
            '/api/articles/', self.article_1, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Titlely', response.data['title'])
        self.assertIn('This is my article', response.data['body'])

    def test_creation_of_invalid_article(self):
        self.mock_login()
        response = self.client.post(
            '/api/articles/', self.invalid_article, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_articles(self):
        response = self.client.get('/api/articles/')
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue('results' in data)
        self.assertIsInstance(data.get('results'), list)

    def test_get_single_article(self):
        self.mock_login()
        self.client.post('/api/articles/', self.article_1, format="json")
        response = self.client.get('/api/articles/titlely')
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertTrue('article' in data)

    def test_getting_innexistent_article(self):
        response = self.client.get('/api/articles/brave-new-world-556')
        self.assertEqual(response.status_code, 404)

    def test_duplication_of_title_by_same_user(self):
        self.mock_login()
        self.client.post('/api/articles/', self.article_1, format="json")
        response = self.client.post(
            '/api/articles/', self.article_1, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            response.data.get('errors')[0],
            "You already have an article with the same title")

    def test_creation_of_existing_title_by_different_user(self):
        self.different_user_mock_login()
        response = self.client.post(
            '/api/articles/', self.article_1, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('Titlely', response.data['title'])

    def test_deletion_of_article_by_owner(self):
        self.mock_login()
        self.client.post('/api/articles/', self.article_1, format="json")
        response = self.client.delete('/api/articles/titlely')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('message'), "Article deleted successfully")

    def test_deletion_of_article_by_non_owner(self):
        self.mock_login()
        self.client.post('/api/articles/', self.article_1, format="json")
        self.different_user_mock_login()
        response = self.client.delete('/api/articles/titlely')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('You do not have rights to delete',
                      response.data.get('message'))

    def test_update_of_article_by_owner(self):
        self.mock_login()
        self.client.post('/api/articles/', self.article_1, format="json")
        edit_response = self.client.put(
            '/api/articles/titlely', self.modified_article, format="json")
        get_response = self.client.get('/api/articles/modified-title')
        data = get_response.data.get('article')
        self.assertEqual(edit_response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), "Modified title")
        self.assertEqual(
            data.get('description'), "The description is also different")

    def test_rating_an_article(self):
        self.mock_login()
        self.client.post("/api/articles/", self.article_1, format="json")
        self.different_user_mock_login()
        rating_response = self.client.put(
            '/api/articles/titlely/rate_article/',
            self.article_rating_4,
            format="json")
        get_response = self.client.get('/api/articles/titlely')
        data = get_response.data.get('article')

        self.assertEqual(rating_response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('rating'), 4)
        self.assertEqual(data.get('ratingsCount'), 1)

    def test_rating_score_is_average_of_all_ratings(self):
        self.mock_login()
        self.client.post("/api/articles/", self.article_1, format="json")
        self.different_user_mock_login()
        rating_response_1 = self.client.put(
            '/api/articles/titlely/rate_article/',
            self.article_rating_4,
            format="json")
        rating_response_2 = self.client.put(
            '/api/articles/titlely/rate_article/',
            self.article_rating_5,
            format="json")
        get_response = self.client.get('/api/articles/titlely')
        data = get_response.data.get('article')

        self.assertEqual(rating_response_1.status_code,
                         status.HTTP_202_ACCEPTED)
        self.assertEqual(rating_response_2.status_code,
                         status.HTTP_202_ACCEPTED)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('rating'), 4.5)
        self.assertEqual(data.get('ratingsCount'), 2)

    def test_user_rates_own_article(self):
        self.mock_login()
        self.client.post("/api/articles/", self.article_1, format="json")
        rating_response = self.client.put(
            '/api/articles/titlely/rate_article/',
            self.article_rating_4,
            format="json")
        get_response = self.client.get('/api/articles/titlely')
        data = get_response.data.get('article')

        self.assertEqual(rating_response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('rating'), 0)
        self.assertEqual(data.get('ratingsCount'), 0)

    def test_user_rating_out_of_range(self):
        self.mock_login()
        self.client.post("/api/articles/", self.article_1, format="json")
        self.different_user_mock_login()
        rating_response = self.client.put(
            '/api/articles/titlely/rate_article/',
            self.article_rating_6,
            format="json")
        get_response = self.client.get('/api/articles/titlely')
        data = get_response.data.get('article')

        self.assertEqual(rating_response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('rating'), 0)
        self.assertEqual(data.get('ratingsCount'), 0)

    def test_liking_articles(self):
        """This method tests for liking an article"""
        self.mock_login()
        self.client.post("/api/articles/", self.article_1, format="json")
        response = self.client.post(
            "/api/articles/titlely/like/", self.like_article, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert "username" in response.data
        assert "action" in response.data
        assert "article" in response.data

    def test_updating_disliking_articles(self):
        """This method tests for updating liking an article"""
        self.mock_login()
        self.client.post("/api/articles/", self.article_1, format="json")
        response = self.client.post(
            "/api/articles/titlely/like/", self.like_article, format="json")
        response = self.client.put(
            '/api/articles/titlely/like/', self.dislike_article, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert "username" in response.data
        assert "action" in response.data
        assert "article" in response.data

    def test_liking_article_twice(self):
        """This method tests for updating liking an article"""
        self.mock_login()
        self.client.post("/api/articles/", self.article_1, format="json")
        self.client.post(
            "/api/articles/titlely/like/", self.like_article, format="json")
        response1 = self.client.post(
            '/api/articles/titlely/like/', self.dislike_article, format="json")
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        assert "errors" in response1.data

    def test_updating_liking_article_without_liking_first(self):
        """This method tests for updating liking an article"""
        self.mock_login()
        self.client.post("/api/articles/", self.article_1, format="json")
        response1 = self.client.put(
            '/api/articles/titlely/like/', self.dislike_article, format="json")
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        assert "errors" in response1.data

    def test_get_comments_status_code(self):
        self.mock_login()
        self.client.post('/api/articles/', self.article_1, format="json")
        response = self.client.get('/api/articles/titlely/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_comments_status_code(self):
        self.mock_login()
        self.client.post('/api/articles/', self.article_1, format="json")
        response = self.client.post(
            '/api/articles/titlely/comments/',
            data={"comment": {
                "body": "something else"
            }},
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_child_comments_status_code(self):
        self.mock_login()
        self.client.post('/api/articles/', self.article_1, format="json")
        self.client.post(
            '/api/articles/titlely/comments/',
            data=self.comment1,
            format="json")
        response = self.client.post(
            '/api/articles/titlely/comments/4/',
            data={"reply": {
                "body": "something else"
            }},
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_favouriting_article(self):
        """This method tests favourating an article"""
        self.mock_login()
        self.client.post("/api/articles/", self.article_1, format="json")
        response = self.client.post(
            "/api/articles/titlely/favourite/", format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert "message" in response.data

    def test_getting_favourite_articles(self):
        """This method tests favourating an article"""
        self.mock_login()
        self.client.post("/api/articles/", self.article_1, format="json")
        self.client.post("/api/articles/titlely/favourite/", format="json")
        response = self.client.get("/api/articles/favourites/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert "favourites" in response.data

    def test_favouriting_article_twice(self):
        """This method tests favourating an article"""
        self.mock_login()
        self.client.post("/api/articles/", self.article_1, format="json")
        self.client.post("/api/articles/titlely/favourite/", format="json")
        response = self.client.post(
            "/api/articles/titlely/favourite/", format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert "errors" in response.data

    def test_unfavouriting_article(self):
        """This method tests favourating an article"""
        self.mock_login()
        self.client.post("/api/articles/", self.article_1, format="json")
        self.client.post("/api/articles/titlely/favourite/", format="json")
        response = self.client.delete(
            "/api/articles/titlely/favourite/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert "status" in response.data

    def test_unfavouriting_article_not_favourated(self):
        """This method tests favourating an article"""
        self.mock_login()
        self.client.post("/api/articles/", self.article_1, format="json")
        response = self.client.delete(
            "/api/articles/titlely/favourite/", format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert "error" in response.data

    def test_search_article_by_author(self):
        # create two articles using one user
        self.mock_login()
        self.create_article(self.article_1)
        self.create_article(self.article_2)
        # create two more article with a different user
        self.different_user_mock_login()
        self.create_article(self.article_3)
        self.create_article(self.article_4)
        author = self.reg_data.get('user')['username']
        # get the articles of the first user
        response = self.client.get(
            '/api/articles/search/?author={}'.format(author))
        self.assertEqual(len(response.data['search results']), 2)
        self.assertEqual(response.status_code, 200)

    def test_search_article_by_title(self):
        # create two articles using one user
        self.mock_login()
        self.create_article(self.article_1)
        self.create_article(self.article_2)
        self.create_article(self.article_3)
        title = self.article_2.get('article')['title']
        response = self.client.get(
            '/api/articles/search/?title={}'.format(title))
        self.assertEqual(len(response.data['search results']), 1)
        self.assertIn(title, str(response.data))

    def test_search_article_by_tag(self):
        self.mock_login()
        self.create_article(self.article_1)
        self.create_article(self.article_2)
        response = self.client.get('/api/articles/search/?tag=Health')
        self.assertEqual(len(response.data['search results']), 1)
        self.assertEqual(response.status_code, 200)

    def test_search_article_by_keywords(self):
        self.mock_login()
        self.create_article(self.article_1)
        self.create_article(self.article_2)
        self.create_article(self.article_3)

        response = self.client.get('/api/articles/search/?keywords=title')
        self.assertEqual(len(response.data['search results']), 2)
        self.assertEqual(response.status_code, 200)

    def search_article_with_all_parameters(self):
        # create two articles using one user
        self.mock_login()
        self.create_article(self.article_1)
        self.create_article(self.article_2)
        self.create_article(self.article_3)
        self.create_article(self.article_4)
        author = self.reg_data.get('user')['username']
        tag = 'Hello'
        keywords = 'let,see'
        response = self.client.get(
            '/api/articles/search/?author={}&tag={}&keywords={}'.format(
                author, tag, keywords))
        self.assertEqual(len(response.data['search results']), 1)
        self.assertEqual(response.status_code, 200)
