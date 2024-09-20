from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model=Review
        fields='__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=Profile
        fields='__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model=Tag
        fields='__all__'



#so in the below class we create a serializer for the model we want to serialize and the fields
class ProjectSerializer(serializers.ModelSerializer):

    #to get the information of the owner also in the data
    owner=ProfileSerializer(many=False)
    tags=TagSerializer(many=True)


    #so if we want some other models to be included in the json response of some other model
    #we first create a serialize method field then we create a function like below starting with get which serializes the data
    #and then the data is added to the json response
    reviews=serializers.SerializerMethodField()

    class Meta:
        model=Project
        fields='__all__'

    
    #the method name of a serializerMethodField should always start with a get
    def get_reviews(self, obj):

        reviews=obj.review_set.all()
        serializer=ReviewSerializer(reviews, many=True)
        return serializer.data


