from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

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
    user=instance.user
    user.delete()
    print('deleteing user....')


#on postsave we want to trigger the method which will be called
#and we mention the model which will trigger it
post_save.connect(createProfile,sender=User)
post_delete.connect(deleteUser,sender=Profile)