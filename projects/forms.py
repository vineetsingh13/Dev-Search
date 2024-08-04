from django.forms import ModelForm
from .models import Project

#so basically what happens is using Django ModelForm we pass the model whose form we want to create and the fields we want
#so based on the attribute type in models django automatically creates a form
#if we use __all__ it will generate field for all attributes if we want some specific fields we mention them in a list as strings
class ProjectForm(ModelForm):
    class Meta:

        model=Project
        #field=['']
        fields='__all__'