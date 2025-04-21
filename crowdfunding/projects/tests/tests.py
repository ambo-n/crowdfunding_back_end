from django.test import TestCase
from projects.models import Project, Category, Pledge
from projects.serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, PledgeDetailSerializer, CategorySerializer, CategoryDetailSerializer
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", email= "test_user@mail.com",password="password123")
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
class PledgeModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser",email= "test_user@mail.com", password="password123")
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
class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(description="Test category")
        self.assertEqual(category.description, "Test category")
class PledgeSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", email= "test_user@mail.com", password="password123")
        self.donor = get_user_model().objects.create_user(username="pledgemaker",email= "pledge_user@mail.com", password="pledger123")
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
        self.pledge = Pledge.objects.create(
            amount = 5000,
            comment = "test pledge",
            anonymous = False,
            project = self.project,
            support = self.donor
        )
        self.pledge2 = Pledge.objects.create(
            amount = 5000,
            comment = "test pledge2",
            anonymous = False,
            project = self.project,
            support = self.donor
        )
    
    def test_pledge_serializer(self):
        serializer = PledgeSerializer(self.pledge)
        data = serializer.data
        self.assertEqual(data["amount"], 5000)
        self.assertEqual(data["comment"], "test pledge")
        self.assertEqual(data["support"], self.donor.id)
    
    def test_pledge_deserialization(self):
        data = {
            "amount":1000,
            "comment":"Keep up the good work",
            "anonymous":True,
            "project":self.project.id,
            "support":self.donor
        }
        serializer= PledgeSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        invalid_data = {
            "amount":1000,
            "project":self.project,
            "support":self.donor
            
        }
        serializer = PledgeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)
    
    def test_pledge_update(self):
        pledge = Pledge.objects.get(pk=self.pledge2.id)
        pledge.amount = 800
        pledge.comment = "Keep up the good work updated"
        pledge.anonymous = False
        pledge.save()
        serializer = PledgeDetailSerializer(pledge)
        data = serializer.data
        self.assertEqual(data["amount"], 800)
        self.assertEqual(data["comment"], "Keep up the good work updated")
        self.assertFalse(data["anonymous"])
    

    def test_project_detail_serializer(self):
        serializer = ProjectDetailSerializer(self.project)
        data = serializer.data
        self.assertEqual(data["pledges"][0]["amount"], 5000)
        self.assertEqual(len(data["pledges"]), 2)

class ProjectSerializerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser",email= "test_user@mail.com", password="password123")
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
    
    def test_project_update_serializer(self):
        project = Project.objects.get(pk=self.project.id)
        project.title="Test Project Update"
        project.description="An updated descriptor"
        project.goal=80
        project.is_open=False
        project.save()
        
        serializer = ProjectDetailSerializer(project)
        data = serializer.data
        self.assertEqual(data["title"],"Test Project Update")
        self.assertEqual(data["description"], "An updated descriptor")
        self.assertFalse(data["is_open"])
    
class CategorySerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(description="Test Category")

    def test_category_serializer(self):
        serializer = CategorySerializer(self.category)
        data = serializer.data
        self.assertEqual(data["description"], "Test Category")
        self.assertEqual(data["id"],self.category.id)
    
    def test_category_deserialization(self):
        data = {
            "description":"Environment"
        }
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        invalid_data = {
            "amount":5000
        }
        serializer2 = CategorySerializer(data=invalid_data)
        self.assertFalse(serializer2.is_valid(), serializer2.errors)

    def test_category_update(self):
        category = Category.objects.get(pk=self.category.id)
        category.description = "Updated test category description"
        category.save()
        serializer = CategoryDetailSerializer(category)
        data = serializer.data
        self.assertEqual(category.description, "Updated test category description")

class ProjectAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username="testuser",email= "test_user@mail.com", password="password123")
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
    
    def test_get_single_project(self):
        url = reverse("project-detail",kwargs={"pk":self.project.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"],"Test Project")
        self.assertEqual(len(response.data),17)
        
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
    
    def test_create_project_invalid(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("project-list")
        data ={
            "title": "New Project",
            "description": "A new project description",
            "image": "https://example.com/new.jpg",
            "is_open": True,
            "address": "37 Halsey Road",
	        "suburb": "Tunkalilla",
	        "postcode": "5203",
	        "state": "SA",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("category", response.data)
        self.assertEqual(response.data["category"][0], "This field is required.")
        self.assertIn("goal", response.data)
        self.assertEqual(response.data["goal"][0], "This field is required.")
    
    def test_update_project(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("project-detail", kwargs={"pk": self.project.id})
        data = {
            "description":"Updated description for the sample project",
            "goal":10000
        }
        response = self.client.put(url, data, format="json")
        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["goal"], 10000)
        self.assertEqual(response.data["description"], "Updated description for the sample project")
        self.assertEqual(response.data["title"], "Test Project")
        self.assertEqual(response.data["address"],"37 Halsey Road")

    def test_delete_project(self):
        self.client.force_authenticate(user=self.user)
        post_url = reverse("project-list")
        data = {
            "title": "Project to delete",
            "description": "A new project description",
            "goal": 500,
            "image": "https://example.com/new.jpg",
            "is_open": True,
            "address": "37 Halsey Road",
	        "suburb": "Tunkalilla",
	        "postcode": "5203",
	        "state": "SA",
            "category": [self.category.id],
        }
        post_response = self.client.post(post_url,data,format="json")
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post_response.data["title"], "Project to delete")
        delete_url = reverse("project-detail", kwargs={"pk":post_response.data["id"]})
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        get_response = self.client.get(delete_url)
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
        project_count_after_deletion = Project.objects.count()
        self.assertEqual(project_count_after_deletion,1)

class PlegeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username="testuser",email= "test_user@mail.com", password="password123")
        self.donor = get_user_model().objects.create_user(username="testdonor",email= "test_donor@mail.com", password="password123")
        self.admin_user = get_user_model().objects.create_user(username="admin",email= "test_admin@mail.com", password="sth123", is_staff=True, is_superuser=True)
        self.category = Category.objects.create(description="Environment")
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
        self.pledge = Pledge.objects.create(
            amount = 5000,
            comment = "test pledge",
            anonymous = False,
            project = self.project,
            support = self.donor
        )
    def test_get_pledges_authenticated(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("pledge-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["project"], self.project.id)
    def test_get_pledges_unauthenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("pledge-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    def test_create_pledges_authenticated(self):
        self.client.force_authenticate(user=self.donor)
        url = reverse("pledge-list")
        project_url = reverse("project-detail", kwargs={"pk":self.project.id})
        data = {
            "amount": 1000,
            "comment": "Bye weeds",
            "anonymous": False,
            "project": self.project.id,
        }
        response = self.client.post(url, data, format="json")
        get_project_response = self.client.get(project_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pledge.objects.count(), 2)
        self.assertEqual(len(get_project_response.data["pledges"]), 2)
        self.assertEqual(get_project_response.data["pledges"][1]["comment"],"Bye weeds")
        self.assertEqual(get_project_response.data["pledges"][0]["comment"],"test pledge")
    def test_create_pledge_unauthenticated(self):
        url = reverse("pledge-list")
        data = {
            "amount": 1000,
            "comment": "Bye weeds",
            "anonymous": False,
            "project": self.project.id,
        }
        response = self.client.post(url,data,format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_create_pledge_invalid_data(self):
        self.client.force_authenticate(user=self.donor)
        url = reverse("pledge-list")
        data ={
            "title": "New Project",
            "amount": 100.80,
            "comment": "Bye weeds",
            "anonymous": False,
            "project": self.project.id,
        }
        response = self.client.post(url,data,format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_get_detail_on_one_pledge(self):
        self.client.force_authenticate(user=self.donor)
        url = reverse("pledge-detail", kwargs={"pk":self.pledge.id})
        invalid_url = reverse("pledge-detail", kwargs={"pk":8})
        response = self.client.get(url)
        invalid_url_response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(invalid_url_response.status_code, status.HTTP_404_NOT_FOUND)
    def test_update_pledge(self):
        self.client.force_authenticate(user=self.donor)
        url = reverse("pledge-detail", kwargs={"pk":self.pledge.id})
        data ={
            "comment":"updated comment for the test pledge",
            "anonymous":True
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["comment"],"updated comment for the test pledge")
        self.assertTrue(response.data["anonymous"])
        self.assertEqual(Pledge.objects.count(),1)
    def test_delete_pledge(self):
        self.client.force_authenticate(user=self.donor)
        url = reverse("pledge-detail", kwargs={"pk":self.pledge.id})
        response = self.client.delete(url)
        after_deletion_response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(after_deletion_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Pledge.objects.count(),0)
class CategoryAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(description="Environment")
        self.admin_user = get_user_model().objects.create_user(username="admin",email= "test_admin@mail.com",password="sth134",is_staff=True, is_superuser=True)
    def test_get_category(self):
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["description"], "Environment")

    def test_get_a_category(self):
        url = reverse("category-detail",kwargs={"pk":self.category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"],"Environment")
        
    def test_create_category_valid_data(self):
        url = reverse("category-list")
        data ={"description":"Trail"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["description"], "Trail")
        self.assertEqual(Category.objects.count(),2)

    def test_create_category_invalid_data(self):
        url = reverse("category-list")
        data ={"title":"Trail"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Category.objects.count(),1)
    def test_update_category_valid_data(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("category-detail", kwargs={"pk":self.category.id})
        data = {
            "description":"Updated to Ocean"
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "Updated to Ocean")
    def test_update_category_invalid_data(self):
        # self.client.force_authenticate(user=self.admin_user)
        # url = reverse("category-detail", kwargs={"pk":self.category.id})
        # data = {
        #     "title": "sth else"
        # }
        # response = self.client.put(url, data, format="json")
        pass
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_delete_category(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("category-detail",kwargs={"pk":self.category.id})
        response = self.client.delete(url)
        get_delete_url_response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(),0)
        self.assertEqual(get_delete_url_response.status_code, status.HTTP_404_NOT_FOUND)