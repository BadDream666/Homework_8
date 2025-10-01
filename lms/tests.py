from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import Group

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonCRUDTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей через кастомный менеджер
        self.user = User.objects.create_user(
            email='user@test.com',
            password='testpass123'
        )
        self.moderator = User.objects.create_user(
            email='moderator@test.com',
            password='modpass123'
        )
        self.other_user = User.objects.create_user(
            email='other@test.com',
            password='otherpass123'
        )

        # Создаем группу модераторов и добавляем пользователя
        self.moder_group = Group.objects.create(name='moders')
        self.moderator.groups.add(self.moder_group)

        # Создаем тестовые данные
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            owner=self.user
        )

        self.lesson_data = {
            'name': 'Test Lesson',
            'description': 'Test Lesson Description',
            'course': self.course.id,
            'video_link': 'https://www.youtube.com/watch?v=test123',
        }

    def test_create_lesson_authenticated_user(self):
        """Тест создания урока аутентифицированным пользователем"""
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('lesson-create'),
            data=self.lesson_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.get().owner, self.user)

    def test_create_lesson_with_invalid_link(self):
        """Тест создания урока с невалидной ссылкой"""
        self.client.force_authenticate(user=self.user)

        invalid_data = self.lesson_data.copy()
        invalid_data['video_link'] = 'https://vk.com/video123'

        response = self.client.post(
            reverse('lesson-create'),
            data=invalid_data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_link', response.data)

    def test_create_lesson_moderator_forbidden(self):
        """Тест что модератор не может создавать уроки"""
        self.client.force_authenticate(user=self.moderator)

        response = self.client.post(
            reverse('lesson-create'),
            data=self.lesson_data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_lessons_owner(self):
        """Тест списка уроков для владельца"""
        lesson = Lesson.objects.create(
            name='Test Lesson',
            course=self.course,
            owner=self.user,
            video_link='https://www.youtube.com/watch?v=test'
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('lesson-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_lessons_moderator(self):
        """Тест списка уроков для модератора (видит все)"""
        Lesson.objects.create(
            name='Test Lesson',
            course=self.course,
            owner=self.user,
            video_link='https://www.youtube.com/watch?v=test'
        )

        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(reverse('lesson-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            name='Test Course',
            owner=self.user
        )

    def test_subscribe_to_course(self):
        """Тест подписки на курс"""
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('course-subscribe', kwargs={'pk': self.course.id})
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
        self.assertEqual(response.data['status'], 'subscribed')

    def test_subscribe_already_subscribed(self):
        """Тест повторной подписки на курс"""
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('course-subscribe', kwargs={'pk': self.course.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'already subscribed')

    def test_unsubscribe_from_course(self):
        """Тест отписки от курса"""
        Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('course-unsubscribe', kwargs={'pk': self.course.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
        self.assertEqual(response.data['status'], 'unsubscribed')

    def test_unsubscribe_not_subscribed(self):
        """Тест отписки когда не подписан"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('course-unsubscribe', kwargs={'pk': self.course.id})
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'not subscribed')

    def test_course_serializer_with_subscription(self):
        """Тест сериализатора курса с информацией о подписке"""
        subscription = Subscription.objects.create(user=self.user, course=self.course)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse('course-detail', kwargs={'pk': self.course.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])


class PermissionTestCase(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(email='owner@test.com', password='pass')
        self.other_user = User.objects.create_user(email='other@test.com', password='pass')
        self.moderator = User.objects.create_user(email='mod@test.com', password='pass')

        moder_group = Group.objects.create(name='moders')
        self.moderator.groups.add(moder_group)

        self.course = Course.objects.create(name='Test Course', owner=self.owner)
        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            course=self.course,
            owner=self.owner,
            video_link='https://www.youtube.com/watch?v=test'
        )

    def test_owner_can_delete_lesson(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(
            reverse('lesson-destroy', kwargs={'pk': self.lesson.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_moderator_can_delete_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(
            reverse('lesson-destroy', kwargs={'pk': self.lesson.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_owner_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(
            reverse('lesson-destroy', kwargs={'pk': self.lesson.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class YouTubeValidatorTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            name='Test Course',
            owner=self.user
        )

    def test_valid_youtube_links(self):
        """Тест валидных YouTube ссылок"""
        valid_links = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://youtube.com/watch?v=test123',
            'https://youtu.be/dQw4w9WgXcQ',
            'http://www.youtube.com/watch?v=test',
        ]

        self.client.force_authenticate(user=self.user)

        for link in valid_links:
            data = {
                'name': f'Lesson with {link}',
                'course': self.course.id,
                'video_link': link,
            }
            response = self.client.post(reverse('lesson-create'), data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_links(self):
        """Тест невалидных ссылок"""
        invalid_links = [
            'https://vk.com/video123',
            'https://rutube.ru/video/123',
            'https://example.com/video',
        ]

        self.client.force_authenticate(user=self.user)

        for link in invalid_links:
            data = {
                'name': f'Lesson with {link}',
                'course': self.course.id,
                'video_link': link,
            }
            response = self.client.post(reverse('lesson-create'), data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
