from django.test import TestCase
from users.models import CustomUser
from django.core.exceptions import ValidationError

class UserModelTest(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username="test_user",
            password="testpassword123",
            email="test_user@mail.com"
        )
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.email, "test_user@mail.com")
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)
    
    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            username="admin_user",
            password="adminpassword123",
            email="admin_user@mail.com"
        )
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_active)

    def test_user_str_representation(self):
        user = CustomUser.objects.create_user(
            username="test_user",
            password="testpassword123",
            email="test_user@mail.com"
        )
        self.assertEqual(str(user),"test_user")
    
    def test_missing_username(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
            username="",
            password="testpassword123",
            email="test_user@mail.com"
            )
    def test_missing_email(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
            username="test_user",
            password="123",
            email=""
            )
            