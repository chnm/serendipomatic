from django.db import models

# Create your models here.


class ZoteroUser(models.Model):
    # username, userid, token
    username = models.CharField(max_length=255, unique=True)
    userid = models.CharField(max_length=255, unique=True)
    token = models.CharField(max_length=255)

    # TODO: __unicode__ method (username?)

    def __repr__(self):
        return '<ZoteroUser %s>' % self.username


# examples code
# from smartstash.auth.models import ZoteroUser
#
# find specific user by username:
# ZoteroUser.objects.get(username='rlskoeser')
# raises does not exist exception: https://docs.djangoproject.com/en/1.2/ref/exceptions/#objectdoesnotexist-and-doesnotexist
# create a new one:
# zu = ZoteroUser(username='rlskoeser')
# zu.save()
