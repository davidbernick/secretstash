from django.db import models
from django.contrib.auth.models import User,Group
from guardian.shortcuts import assign_perm,remove_perm
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save,post_syncdb
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import random,string

def id_generator(size=18, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Host(models.Model):
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(User)
    apikey = models.ForeignKey(Token,null=True, blank=True)
    
    #save! create user
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(Host,self).save(*args, **kwargs)
        else:
            user = User.objects.create_user(self.name, self.name+"@"+"randomhost.com", id_generator())
            self.owner=user
            token = Token.objects.get(user=user)
            self.apikey=token
            super(Host,self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        permissions = (
            ('view_host', 'View Host'),
        )

class Secret(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True,unique=True)
    description = models.CharField(max_length=100,blank=True,null=True)
    content = models.TextField()
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        permissions = (
            ('view_secret', 'View Secret'),
        )
