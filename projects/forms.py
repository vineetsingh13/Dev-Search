from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList
from .models import Project, Review
from django import forms

#so basically what happens is using Django ModelForm we pass the model whose form we want to create and the fields we want
#so based on the attribute type in models django automatically creates a form
#if we use __all__ it will generate field for all attributes if we want some specific fields we mention them in a list as strings
class ProjectForm(ModelForm):
    class Meta:

        model=Project
        fields=['title','featured_image', 'description','demo_link','source_link','tags']
        #fields='__all__'

        #to choose the widget we want with each field in the form
        widgets={
            'tags':forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self,*args,**kwargs):
        super(ProjectForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

        #for accessing each field in the form & update class, widget, etc
        #self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add title'})


class ReviewForm(ModelForm):

    class Meta:
        model=Review
        fields=['value','body']

        labels={
            'value':'Place your vote',
            'body':'Add a comment'
        }
    
    def __init__(self,*args,**kwargs):
        super(ReviewForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})