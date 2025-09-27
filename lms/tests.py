from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import Group

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@test.com',
            password='testpass'
        )
        self.moderator = User.objects.create(
            email='moderator@test.com',
            password='modpass'
        )

        moder_group, created = Group.objects.get_or_create(name='moders')
        self.moderator.groups.add(moder_group)

        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Test Lesson Description',
            course=self.course,
            video_link='https://www.youtube.com/watch?v=test',
            owner=self.user
        )

    def test_lesson_create_valid_youtube(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'New Lesson',
            'description': 'New Description',
            'course': self.course.id,
            'video_link': 'https://www.youtube.com/watch?v=new',
        }

        response = self.client.post(
            reverse('lesson-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_create_invalid_link(self):
        self.client.force_authenticate(user=self.user)

        data = {
            'name': 'Wrong Link Lesson',
            'description': 'Wrong Link',
            'course': self.course.id,
            'video_link': 'https://vk.com/video123',
        }

        response = self.client.post(
            reverse('lesson-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_subscription_flow(self):
        self.client.force_authenticate(user=self.user)

        # Subscribe
        response = self.client.post(
            reverse('course-subscribe', kwargs={'pk': self.course.id})
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Unsubscribe
        response = self.client.post(
            reverse('course-unsubscribe', kwargs={'pk': self.course.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())


class PermissionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='user@test.com', password='pass')
        self.other_user = User.objects.create(email='other@test.com', password='pass')
        self.moderator = User.objects.create(email='mod@test.com', password='pass')

        moder_group, created = Group.objects.get_or_create(name='moders')
        self.moderator.groups.add(moder_group)

        self.course = Course.objects.create(name='Test Course', owner=self.user)
        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            course=self.course,
            owner=self.user,
            video_link='https://www.youtube.com/watch?v=test'
        )

    def test_owner_can_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('lesson-destroy', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_owner_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(reverse('lesson-destroy', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
