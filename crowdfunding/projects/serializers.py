from rest_framework import serializers
from django.apps import apps
# from .models import Category

class PledgeSerializer(serializers.ModelSerializer):
    support = serializers.ReadOnlyField(source='support.id')
    class Meta:
        model = apps.get_model('projects.Pledge')
        fields ='__all__'

class PledgeDetailSerializer(PledgeSerializer):
    def update(self,instance,validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.comment = validated_data.get('comment',instance.comment)
        instance.anonymous = validated_data.get('anonymous', instance.anonymous)
        instance.project = validated_data.get('project',instance.project)
        instance.support = validated_data.get('suppport',instance.support)
        instance.save()
        return instance
class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = apps.get_model('projects.Project')
        fields='__all__'

class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description =validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        # if 'category' in validated_data:
        #     category_data = validated_data.pop('category')
        #     instance.category.set(category_data)
        instance.save()
        return instance
    
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = apps.get_model('projects.Category')
#         fields='__all__'

# class CategoryDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = apps.get_model('projects.Category')
#         fields='__all__'
#     projects = ProjectSerializer(many=True, read_only=True)

#     def update(self, instance, validated_data):
#         instance.description = validated_data.get('description', instance.description)
#         instance.save()
#         return instance
