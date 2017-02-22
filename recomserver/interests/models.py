from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings



class Interest(models.Model):
    name = models.CharField(_('Interest Name'), max_length=255)

class InterestUser(models.Model):
    interest = models.ForeignKey(Interest)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

class UserInterestHash(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    phash = models.BigIntegerField()
    phash_hex = models.TextField(default=None, null=True)


