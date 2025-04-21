from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from users.models import CustomUser
from django.urls import reverse
from rest_framework import status

class CustomUserAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="test_user",
            password="testpassword123",
            email="test_user@mail.com"
        )
        cls.admin = CustomUser.objects.create_superuser(
            username="admin_user",
            password="adminpassword123",
            email="admin_user@mail.com"
        )
    
    def test_get_users(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("users-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_post_users(self):
        url = reverse("users-list")
        data = {
            "username":"NewUser1",
            "password":"NewUserPass1",
            "email":"hi@mail.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"],"NewUser1")
        self.assertEqual(CustomUser.objects.count(),3)
        self.assertTrue(CustomUser.objects.filter(username="NewUser1").exists())
    
    def test_create_user_missing_email(self):
        url = reverse("users-list")
        data = {
            "username":"NewUser1",
            "password":"NewUserPass1",}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(),2)
        self.assertIn("email", response.data)
    def test_create_user_invalid_email(self):
        url = reverse("users-list")
        data = {
            "username":"NewUser1",
            "password":"NewUserPass1",
            "email":"newuser1"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(CustomUser.objects.count(),2)
        self.assertIn("email", response.data)


class CustomUserDetailAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            username="test_user",
            password="testpassword123",
            email="test_user@mail.com"
        )
        cls.admin = CustomUser.objects.create_superuser(
            username="admin_user",
            password="adminpassword123",
            email="admin_user@mail.com"
        )
    def test_get_one_user(self):
        url = reverse("user-details", kwargs={"pk":self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertFalse(response.data["is_superuser"])
    
    def test_update_user_detail_authenticated(self):
        url = reverse("user-details", kwargs={"pk":self.user.id})
        self.client.force_authenticate(user=self.user)
        data = {
            "first_name": "Ashley",
            "last_name":"Wilson"
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"],self.user.id)
        self.assertEqual(response.data["first_name"],"Ashley")
        self.assertEqual(response.data["last_name"],"Wilson")
        self.assertEqual(response.data["username"],self.user.username)

    def test_update_user_detail_unauthenticated(self):
        url = reverse("user-details", kwargs={"pk":self.user.id})
        data = {
            "first_name": "Ashley",
            "last_name":"Wilson"
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_cannot_update_another_user(self):
        other_user = CustomUser.objects.create_user(
            username="other_user",
            password="password1233",
            email="other@mail.com"
        )
        self.client.force_authenticate(user=other_user)
        url = reverse("user-details", kwargs={"pk":self.user.id})
        response = self.client.put(url, {"first_name":"Amser"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_authenticated(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("user-details", kwargs={"pk":self.user.id})
        response = self.client.delete(url)
        response2 = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(),1)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

class CustomUserTokenAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user (
            username="test_user",
            password="testpassword123",
            email="test_user@mail.com"
        )
    
    def test_get_token(self):
        url = reverse("api_token_auth")
        data={
            "username":"test_user",
            "password":"testpassword123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user_id"], self.user.id)
    
    def test_get_token_with_invalid_credentials(self):
        url = reverse("api_token_auth")
        data={
            "username":"test_user",
            "password":"wrongpass"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)

