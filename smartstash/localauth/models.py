from django.db import models

# Create your models here.

# NOTE: currently unused; probably this will go away when we refactor
# zotero/oauth


class ZoteroUser(models.Model):
    # username, userid, token
    username = models.CharField(max_length=255, unique=True)
    userid = models.CharField(max_length=255, unique=True)
    token = models.CharField(max_length=255)

    def __unicode__(self):
        return self.username

    def __repr__(self):
        return '<ZoteroUser %s>' % self.username

