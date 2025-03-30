from django.test import TestCase
from projects.models import Project, Category, Pledge
from projects.serializers import ProjectSerializer
from django.contrib.auth import get_user_model

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
