from rest_framework import serializers
from projects.models import Project

#so in the below class we create a serializer for the model we want to serialize and the fields
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields='__all__'