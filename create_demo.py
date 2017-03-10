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
from django.db import transaction


if __name__ == '__main__':
    objects_with_interest_count = 10000
    interests_count = 1500
    interest_per_object = 200

    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE interests_objectinterest")
        cursor.execute("TRUNCATE TABLE interests_objectinteresthash")
        cursor.execute("TRUNCATE TABLE interests_objectwithinterest")
        cursor.execute("TRUNCATE TABLE interests_interest")

    with transaction.atomic():
        for i in range(1, objects_with_interest_count):
            print(">>> creating objects with interest", i, "/", objects_with_interest_count)
            ObjectWithInterest.objects.create(object_id=i, object_type='Generic')

        for i in range(1, interests_count):
            print(">>> creating interest", i, "/", interests_count)
            Interest.objects.create(name='interest_%s' % i)

    interests = [i for i in Interest.objects.all()]

    with transaction.atomic():
        total = ObjectWithInterest.objects.count()
        cnt = 0
        for u in ObjectWithInterest.objects.all():
            print(">>> ObjectWithInterest >>>", u.id, cnt, "/", total)
            for interest in [random.choice(interests) for i in range(1, interest_per_object)]:
                ObjectInterest.objects.create(object_id=u.id, interest_id=interest.id)
            cnt += 1

    count = ObjectWithInterest.objects.count()
    cnt = 0
    for object_with_interest in ObjectWithInterest.objects.all():
        print(">>> calculating hash >>>", object_with_interest.id, cnt, "/", count)
        ObjectInterestHash.calc_hash_for_object(object_with_interest)
        cnt += 1


