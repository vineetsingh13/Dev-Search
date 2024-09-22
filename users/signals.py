from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings

#creating a seperate file for signals doesnot make django know when to run these signals
#if we mention these in same files as models.py it will work but here not
#so to make them work we add the signals in apps.py


#@receiver(post_save,sender=Profile)
def createProfile(sender, instance, created,**kwargs):
    #here we are creating a signal that automatically creates a profile when a user is created
    if created:
        user=instance
        profile=Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )

     


def deleteUser(sender, instance,**kwargs):
    #here we are creating a signal when the profile is deleted the user is also deleted
    #below we are trying to delete user as soon as profile is deleted
    #but we have already set oncascade delete in model for profile and user
    #so we would get error here if we dont add this inside try catch block
    try:
        user=instance.user
        user.delete()
        print('deleteing user....')
    except:
        pass


def updateUser(sender,instance,created,**kwargs):

    profile=instance
    user=profile.user

    #we add created condition here because in createProfile() we are already creating the profile
    #so here when we save the user the a signal would be sent to createProfile which will become an infinite loop
    if created == False:
        user.first_name=profile.name
        user.username=profile.username
        user.email=profile.email
        user.save()




#on postsave we want to trigger the method which will be called
#and we mention the model which will trigger it
post_save.connect(createProfile,sender=User)
post_save.connect(updateUser,sender=Profile)
post_delete.connect(deleteUser,sender=Profile)