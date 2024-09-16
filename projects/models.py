from django.db import models
import uuid
from users.models import Profile
# Create your models here.


class Project(models.Model):
    owner=models.ForeignKey(Profile,null=True,blank=True,on_delete=models.SET_NULL)
    title=models.CharField(max_length=200)
    #here null is for the table and blank is for the template
    description=models.TextField(null=True,blank=True)
    featured_image=models.ImageField(null=True,blank=True, default="default.jpg")
    demo_link=models.CharField(max_length=2000,null=True,blank=True)
    source_link=models.CharField(max_length=2000,null=True,blank=True)
    
    #if the tag model is written before the Project model we dont need to use '' else we need to use ''
    tags=models.ManyToManyField('Tag',blank=True)
    vote_total=models.IntegerField(default=0,null=True,blank=True)
    vote_ratio=models.IntegerField(default=0,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    #we use this str to specify the format on how or what value is to be printed when the class is called
    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['-vote_ratio','-vote_total','title']


    def reviewers(self):
        #getting a list of all the owners of project and people who have reviewed to stop them to write further review
        querySet=self.review_set.all().values_list('owner__id',flat=True)
        return querySet

    #adding property makes the function run as an attribute
    @property
    def getVoteCount(self):

        reviews=self.review_set.all()
        upVote=reviews.filter(value='up').count()
        totalVotes=reviews.count()
        ratio=(upVote/totalVotes)*100
        self.vote_total=totalVotes
        self.vote_ratio=ratio
        self.save()
        

class Review(models.Model):
    Vote_type=(
        ('up', 'Up Vote'),
        ('down','Down Vote')
    )

    owner=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    #so using cascade once the project is deleted all the associated reviews are also deleted
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)
    #now the value attribute below is going to be a dropdown list
    value=models.CharField(max_length=200,choices=Vote_type)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.value
    
    
    class Meta:
        #to make sure no instance of review can have the same owner or project
        unique_together=[['owner','project']]

class Tag(models.Model):
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.name
