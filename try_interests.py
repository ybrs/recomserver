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
from recomserver.interests.models import Interest, InterestUser, UserInterestHash
from PIL import Image


def dhash(image, hash_size = 8):
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS,
    )

    pixels = list(image.getdata())

    # Compare adjacent pixels.
    difference = []
    for row in xrange(hash_size):
        for col in xrange(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    # Convert the binary array to a hexadecimal string.
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0

    return ''.join(hex_string)

if __name__ == '__main__':

    # for i in range(1, 100):
    #     print(">>>", i)
    #     u = User(name='user_%s' % i, username='user_%s' % i)
    #     u.save()
    #
    # for i in range(1, 300):
    #     print(">>>", i)
    #     i = Interest(name='interest_%s' % i)
    #     i.save()
    #
    # interests = [i for i in Interest.objects.all()]
    #
    # for u in User.objects.filter(id__lte=100).all():
    #     print(">>> user >>>", u.id)
    #     for interest in [random.choice(interests) for i in range(1, 100)]:
    #         iu = InterestUser()
    #         iu.user = u
    #         iu.interest = interest
    #         iu.save()

    def set_bit(value, bit):
        return value | (1 << bit)


    def clear_bit(value, bit):
        return value & ~(1 << bit)


    def calc_pos_for_int(i, width=64):
        """

        we use a 64x64 pixel rgb image for fingerprint,
        if i > 64*64 then we use the rest to color code.

        this basically gives us a space of
        64x64x255x255x255 = 67,917,312,000 => 67billion different interests

        :param i:
        :param width:
        :return:
        """
        sq = width ** 2
        if i > sq:
            to_coords = i % sq
            to_color = i - to_coords
        else:
            to_coords = i
            to_color = 1

        y = to_coords % width
        x = to_coords / width

        if to_color <= 1:
            to_color = 255 * 255 * 255

        b = to_color & 255
        g = (to_color >> 8) & 255
        r = (to_color >> 16) & 255

        return (x, y, r, g, b)



    # print calc_pos_for_int(65128)
    # exit(0)

    def fingerprint_interests(user):
        """

        :param user:
        :return:
        """
        uis = InterestUser.objects.filter(user=user).all()
        width = height = 64
        im = Image.new("RGB", (width, height))
        for ui in uis:
            x, y, r, g, b = calc_pos_for_int(ui.interest_id)
            print x, y, r, g, b
            im.putpixel((x, y), (r,g,b))
        hash = imagehash.average_hash(im, hash_size=64)
        # hash = dhash(im, hash_size=64)
        print("hash:", len(str(hash)))
        print(">>>", hash.__hash__())
        im.save("tempimages/uid_%s.jpg" % user.id)
        return hash

    # for user in User.objects.filter(id=3).all():
    for user in User.objects.filter(id__lte=100).all():
        print(">>>", user.id)
        phash = fingerprint_interests(user)
        uih = UserInterestHash.objects.filter(user=user).first()
        if not uih:
            uih = UserInterestHash(user=user)
        uih.phash = phash.__hash__()
        uih.phash_hex = str(phash)
        uih.save()

    # imagehash.phash("hello:122334:2333434", hash_size=32)
