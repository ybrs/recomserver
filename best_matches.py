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
    obj = ObjectWithInterest.objects.filter(id=sys.argv[1]).first()
    assert obj
    matches = obj.best_matches(limit=int(sys.argv[2]))
    for match in matches:
        print("match: ", match, match.distance, match.object_id)
