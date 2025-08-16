from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit

User = get_user_model()


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user@mail.ru", username="user")
        self.another_user = User.objects.create(email="user2@mail.ru", username="user2")
        self.user_reward_habit_not_public = Habit.objects.create(
            user=self.user,
            place="test",
            time_to_do="19:00:00",
            action="test",
            duration=1,
            tag_public=False,
            frequency=1,
            tag_pleasant_habit=True,
        )
        self.user_habit = Habit.objects.create(
            user=self.user,
            place="test",
            time_to_do="18:00:00",
            action="test",
            duration=1,
            linked_habit=self.user_reward_habit_not_public,
            frequency=1,
        )

    def test_user_can_create_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:my_habits-list")
        data = {
            "place": "create_test",
            "time_to_do": "19:00:00",
            "action": "create_test",
            "tag_public": False,
            "reward": "create_test",
            "duration": 1,
            "frequency": 1,
        }
        response = self.client.post(url, data)
        response_data = response.json()
        if response.status_code != status.HTTP_201_CREATED:
            print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["place"], data["place"])

    def test_user_can_read_his_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:my_habits-detail", args=[self.user_habit.pk])
        response = self.client.get(url)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["place"], self.user_habit.place)

    def test_another_user_cant_read_not_his_habit(self):
        self.client.force_authenticate(user=self.another_user)
        url = reverse("habits:public_habits-detail", args=[self.user_reward_habit_not_public.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_another_user_can_read_public_habit(self):
        self.client.force_authenticate(user=self.another_user)
        url = reverse("habits:public_habits-detail", args=[self.user_habit.pk])
        response = self.client.get(url)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["place"], self.user_habit.place)

    def test_user_can_update_his_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:my_habits-detail", args=[self.user_habit.pk])
        data = {"place": "new_data"}

        response = self.client.patch(url, data)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["place"], data["place"])

    def test_user_cant_update_not_his_habit(self):
        self.client.force_authenticate(user=self.another_user)
        url = reverse("habits:public_habits-detail", args=[self.user_habit.pk])
        data = {"place": "new_data"}

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_cant_delete_not_his_habit(self):
        self.client.force_authenticate(user=self.another_user)
        url = reverse("habits:public_habits-detail", args=[self.user_habit.pk])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_can_delete_his_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:my_habits-detail", args=[self.user_habit.pk])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
