from django.test import TestCase
from users.models import CustomUser
from projects.models import Project
from users.serializers import CustomUserSerializer, CustomUserDetailSerializer
from rest_framework.exceptions import ValidationError

class UserSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.existing_user = CustomUser.objects.create_user(
            username="test_user",
            password="pass123",
            email="test_user@mail.com"
        )
    
    def test_user_serializer(self):
        serializer = CustomUserSerializer(self.existing_user)
        data = serializer.data
        self.assertEqual(data["username"], "test_user")
        self.assertEqual(data["email"], "test_user@mail.com")
        self.assertEqual(data["id"], self.existing_user.id)
        self.assertNotIn("password", data)
    
    def test_user_deserialisation_valid_data_creates_user(self):
        data ={
            "username": "new_user",
            "password": "securePass123",
            "email": "new_user@mail.com"
        }
        serializer = CustomUserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, "new_user")
        self.assertEqual(user.email,"new_user@mail.com")
        self.assertTrue(user.check_password("securePass123"))
    
    def test_user_deserialisation_invalid_data(self):
        cases = [{
            "data":{
                    "username": "test_user2",
                    "password": "pass",
                    "email": "invalid_email"
            },
            "field":"email",
            "expected_error": "Enter a valid email address."
        },
        {
            "data":{
                    "username": "",
                    "password": "pass",
                    "email": "valid@mail.com"
            },
            "field":"username",
            "expected_error":"This field may not be blank."
        }
        ]
        for case in cases:
            with self.subTest(case=case):
                serializer = CustomUserSerializer(data=case["data"])
                self.assertFalse(serializer.is_valid())
                self.assertIn(case["field"], serializer.errors)
                self.assertIn(case["expected_error"], serializer.errors[case["field"]])
    
    def test_user_deserialization_existing_user_raises_validation_error(self):
        data = {
            "username": "test_user",
            "password": "newpassword123",
            "email": "test_user@mail.com"
        }
        serializer = CustomUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)
        self.assertIn("email", serializer.errors)
        self.assertNotIn("password",serializer.errors)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

class CustomUserDetailSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(
            username="test_user",
            password="testpassword123",
            email="test_user@mail.com"
        )
        cls.project = Project.objects.create(
            title="Test Project",
            description="A sample project",
            goal=5000,
            image="https://example.com/image.jpg",
            is_open=True,
            address= "37 Halsey Road",
	        suburb= "Tunkalilla",
	        postcode= 5203,
	        state="SA",
            owner=cls.user,
        )
    
    def test_custom_user_detail_serializer_fields(self):
        serializer = CustomUserDetailSerializer(self.user)
        data = serializer.data
        self.assertEqual(data["username"],"test_user")
        self.assertEqual(data["email"], "test_user@mail.com")
        self.assertIn("id",data)
        self.assertIn("owned_projects",data)
        self.assertEqual(data["owned_projects"][0]["title"],"Test Project")
    
    def test_custom_user_detail_serializer_updates_data(self):
        updated_data ={
            "username":"updated_user",
            "email":"updated@mail.com"
        }
        serializer = CustomUserDetailSerializer(self.user, data=updated_data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_user = serializer.save()
        self.assertEqual(updated_user.username,"updated_user")
        self.assertEqual(updated_user.email, "updated@mail.com")


