from django.test import TestCase
from projects.models import Project, Category, Pledge
from projects.serializers import ProjectSerializer
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password123")
        self.category = Category.objects.create(description= "Test_category")
    
    def test_create_project(self):
        project = Project.objects.create(
            title="Test Project",
            description="A sample project",
            goal=5000,
            image="https://example.com/image.jpg",
            is_open=True,
            address= "37 Halsey Road",
	        suburb= "Tunkalilla",
	        postcode= 5203,
	        state="SA",
            owner=self.user,
        )
        project.category.add(self.category)
    
        self.assertEqual(project.title, "Test Project")
        self.assertEqual(project.description, "A sample project")
        self.assertEqual(project.goal, 5000)
        self.assertEqual(project.owner.username, "testuser")
        self.assertEqual(project.category.count(), 1)

class ProjectSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password123")
        self.category = Category.objects.create(description= "Test_category")
        self.project = Project.objects.create(
            title="Test Project",
            description="A sample project",
            goal=5000,
            image="https://example.com/image.jpg",
            is_open=True,
            address= "37 Halsey Road",
	        suburb= "Tunkalilla",
	        postcode= 5203,
	        state="SA",
            owner=self.user,
        )
        self.project.category.add(self.category)

    def test_project_serializer(self):
        serializer = ProjectSerializer(self.project)
        data = serializer.data
        self.assertEqual(data["title"],"Test Project")
        self.assertEqual(data["owner"], self.user.id)
        self.assertEqual(data["category"], [self.category.id])
    
    def test_project_deserialization(self):
        data ={
            "title":"Test Project",
            "description": "A sample project",
            "goal": 5000,
            "image":"https://example.com/image.jpg",
            "is_open": True,
            "address": "37 Halsey Road",
	        "suburb": "Tunkalilla",
	        "postcode": 5203,
	        "state":"SA",
            "owner": self.user.id,
            "category": [self.category.id]
        }
        serializer = ProjectSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

class PledgeModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password123")
        self.category = Category.objects.create(description= "Test_category")
        self.project = Project.objects.create(
            title="Test Project",
            description="A sample project",
            goal=5000,
            image="https://example.com/image.jpg",
            is_open=True,
            address= "37 Halsey Road",
	        suburb= "Tunkalilla",
	        postcode= 5203,
	        state="SA",
            owner=self.user,
        )
        self.project.category.add(self.category)
    
    def test_create_pledge(self):
        pledge = Pledge.objects.create(
            amount = 5000,
            comment = "test pledge",
            anonymous = False,
            project = self.project,
            support = self.user
        )
        self.assertEqual(pledge.amount, 5000)
        self.assertEqual(pledge.comment, "test pledge")
        self.assertEqual(pledge.project, self.project)
        self.assertEqual(pledge.support, self.user)

class ProjectAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username="testuser", password="password123")
        self.category = Category.objects.create(description="Education")
        self.project = Project.objects.create(
            title="Test Project",
            description="A sample project",
            goal=5000,
            image="https://example.com/image.jpg",
            is_open=True,
            address= "37 Halsey Road",
	        suburb= "Tunkalilla",
	        postcode= 5203,
	        state="SA",
            owner=self.user,
        )
        self.project.category.add(self.category)

    def test_get_projects(self):
        url = reverse("project-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Project", response.json()[0]["title"])
    
    def test_create_project_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("project-list")
        data = {
            "title": "New Project",
            "description": "A new project description",
            "goal": 7000,
            "image": "https://example.com/new.jpg",
            "is_open": True,
            "address": "37 Halsey Road",
	        "suburb": "Tunkalilla",
	        "postcode": "5203",
	        "state": "SA",
            "category": [self.category.id],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(),2)
    
    def test_create_project_unauthenticated(self):
        url = reverse("project-list")
        data = {
                        "title": "New Project",
            "description": "A new project description",
            "goal": 7000,
            "image": "https://example.com/new.jpg",
            "is_open": True,
            "address": "37 Halsey Road",
	        "suburb": "Tunkalilla",
	        "postcode": "5203",
	        "state": "SA",
            "category": [self.category.id],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Project.objects.count(),1)