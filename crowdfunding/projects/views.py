from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .models import Project, Pledge
from .models import Category
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer, PledgeDetailSerializer
from .serializers import CategorySerializer, CategoryDetailSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminorLimitView, IsSupporterOrReadOnly, IsAdminorViewOnly

class ProjectList(APIView):
    permission_classes =[permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ProjectSerializer(data=request.data)
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Invalid token header. No credentials provided"},
                status=status.HTTP_401_UNAUTHORIZED
                            )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class CategoryList(APIView):
    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class CategoryDetail(APIView):
    permission_classes = [IsAdminorViewOnly]
    def get_object(self,pk):
        try:
            category = Category.objects.get(pk=pk)
            return category
        except Category.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data)
    
    def put(self, request,pk):
        category = self.get_object(pk=pk)
        serializer = CategoryDetailSerializer(
            instance=category,
            data = request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status= status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
    def delete(self,request,pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class ProjectDetail(APIView):

    permission_classes =[
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    def get_object(self, pk):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    
    def put(self,request,pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(
            instance=project,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
    def delete(self,request,pk):
        project = self.get_object(pk)
        project.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

class PledgeList(APIView):
    permission_classes =[IsAdminorLimitView,
                         permissions.IsAuthenticatedOrReadOnly]
    
    def get(self,request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(support=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PledgeDetail(APIView):
    permission_classes = [IsSupporterOrReadOnly]
    def get_object(self,pk):
        try:
            pledge = Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request,pledge)
            return pledge
        except Pledge.DoesNotExist:
            raise Http404
        
    def get(self,request,pk):
        pledge = self.get_object(pk)
        serializer = PledgeDetailSerializer(pledge)
        return Response(serializer.data)
    
    def put(self,request,pk):
        pledge = self.get_object(pk)
        serializer = PledgeDetailSerializer(
            instance = pledge,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )
    def delete(self,request,pk):
        pledge = self.get_object(pk)
        pledge.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)