from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase


from .models import Post

class PostModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Post.objects.create(
            author = test_user,
            title = 'Title of Blog',
            rating=5,
            body = 'Words about the blog',
        )
        test_post.save()

    def test_blog_content(self):
        post = Post.objects.get(id=1)

        self.assertEqual(str(post.author), 'tester')
        self.assertEqual(post.title, 'Title of Blog')
        self.assertEqual(post.rating, 5)
        self.assertEqual(post.body, 'Words about the blog')

class APITest(APITestCase):

    def test_list_FORBIDDIEN(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail(self):

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Post.objects.create(
            author = test_user,
            title = 'Title of Blog',
            rating=5,
            body = 'Words about the blog',
        )
        test_post.save()

        response = self.client.get(reverse('posts_detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'id':1,
            'title': test_post.title,
            'body': test_post.body,
            'rating':test_post.rating,
            'author': test_user.id,
        })

    def  test_loggedin_user(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()
        c = Client()
        logged_in = c.login(username='tester', password='pass')
        self.assertTrue(logged_in)

    def test_create(self):

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

     
        url = reverse('posts_list')
        data = {
            "title":"Testing is Fun!!!",
            "body":"when the right tools are available",
            "rating":5,
            "author":test_user.id,
        }
        self.client.login(username='tester',password='pass')

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, test_user.id)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, data['title'])

    def test_update(self):
        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Post.objects.create(
            author = test_user,
            title = 'Title of Blog',
            rating=5,
            body = 'Words about the blog'
        )

        test_post.save()

        url = reverse('posts_detail',args=[test_post.id])
        data = {
            "title":"Testing is Still Fun!!!",
            "author":test_post.author.id,
            "rating":5,
            "body":test_post.body,
        }
        self.client.login(username='tester',password='pass')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, url)
        self.assertEqual(Post.objects.count(), test_post.id)
        self.assertEqual(Post.objects.get().title, data['title'])


    def test_delete(self):
        """Test the api can delete a post."""

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_post = Post.objects.create(
            author = test_user,
            title = 'Title of Blog',
            rating=5,
            body = 'Words about the blog'
        )

        test_post.save()

        post = Post.objects.get()

        url = reverse('posts_detail', kwargs={'pk': post.id})

        self.client.login(username='tester',password='pass')
        response = self.client.delete(url)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)