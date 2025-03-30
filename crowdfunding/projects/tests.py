from django.test import TestCase
from projects.models import Project, Category
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
        