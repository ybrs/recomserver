# -*- coding: utf-8 -*-

import os
import sys
import random
import imagehash
from PIL import Image

proj_path = "."
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
sys.path.append(proj_path)
os.chdir(proj_path)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from recomserver.users.models import User
from recomserver.interests.models import Interest, ObjectInterest, ObjectInterestHash, ObjectWithInterest
from PIL import Image
from django.db import connection


if __name__ == '__main__':
    objects_with_interest_count = 100
    interests_count = 500

    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE interests_objectinterest")
        cursor.execute("TRUNCATE TABLE interests_objectinteresthash")
        cursor.execute("TRUNCATE TABLE interests_objectwithinterest")
        cursor.execute("TRUNCATE TABLE interests_interest")


    for i in range(1, objects_with_interest_count):
        print(">>>", i)
        object_with_interest = ObjectWithInterest(object_id=i, object_type='Generic')
        object_with_interest.save()

    for i in range(1, interests_count):
        print(">>>", i)
        i = Interest(name='interest_%s' % i)
        i.save()

    interests = [i for i in Interest.objects.all()]

    for u in ObjectWithInterest.objects.all():
        print(">>> ObjectWithInterest >>>", u.id)
        for interest in [random.choice(interests) for i in range(1, len(interests))]:
            iu = ObjectInterest()
            iu.object_id = u.id
            iu.interest_id = interest.id
            iu.save()

    for object_with_interest in ObjectWithInterest.objects.all():
        print(">>>", object_with_interest.id)
        ObjectInterestHash.calc_hash_for_object(object_with_interest)


