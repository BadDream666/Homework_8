from unittest import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User

TestCase.maxDiff = None


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@example.com")
        self.course = Course.objects.create(name="Course_test")
        self.lesson = Lesson.objects.create(
            name="Lesson_test", course=self.course, user=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("lms:Lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        user2 = User.objects.create(email="test2@example.com")
        course2 = Course.objects.create(name="Python", user=user2)
        url = reverse("lms:Lesson_create")
        data = {"name": "Python", "course": course2.pk, "user": user2.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    #
    def test_lesson_update(self):
        url = reverse("lms:Lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Python_update",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Python_update")

    #
    def test_lesson_delete(self):
        url = reverse("lms:Lesson_destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    #
    def test_lesson_list(self):
        url = reverse("lms:Lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": "Lesson_test",
                    "description": None,
                    "picture": None,
                    "video_link": None,
                    "course": self.course.pk,
                    "user": self.user.pk,
                }
            ],
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SubscriptionTastCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@example.com", password="123qwe")
        self.course = Course.objects.create(name="Test", user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse("lms:Subscription_create")
        data = {
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(data, {"message": "Подписка создана"})

    def test_subscription_delete(self):
        url = reverse("lms:Subscription_create")
        data = {
            "course": self.course.pk,
        }
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 0)
        self.assertEqual(data, {"message": "Подписка удалена"})
