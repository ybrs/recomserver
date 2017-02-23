from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from PIL import Image
import imagehash

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

class Interest(models.Model):
    name = models.CharField(_('Interest Name'), max_length=255)

class ObjectInterest(models.Model):
    interest_id = models.BigIntegerField(default=None, null=True)
    object_id = models.BigIntegerField(default=None, null=True)

class ObjectWithInterest(models.Model):
    object_id = models.BigIntegerField()
    object_type = models.CharField(max_length=254)

    def best_matches(self, limit=5):
        # interests_objectinteresthash
        matches = ObjectInterestHash.best_matches_for(self, limit=limit)
        ids = [m.object_id for m in matches]

        objects = ObjectWithInterest.objects.filter(object_id__in=ids).all()
        for i, obj in enumerate(objects):
            obj.distance = matches[i].distance
        return objects

    def __repr__(self):
        return '<ObjectWithInterest id=%s object_id=%s>' % (self.id, self.object_id)

class ObjectInterestHash(models.Model):
    object_id = models.BigIntegerField(default=None, null=True)
    phash = models.BigIntegerField()
    phash_hex = models.TextField(default=None, null=True)

    @classmethod
    def best_matches_for(cls, instance, limit=5):
        return ObjectInterestHash.objects.raw("""
            select id, object_id,
                BIT_COUNT(phash ^ (select phash from interests_objectinteresthash where object_id=%s)) as distance
                from interests_objectinteresthash
                order by distance limit %s
        """, [instance.id, limit])

    @classmethod
    def calc_hash_for_object(cls, instance):
        phash = cls.fingerprint_interests(instance, save_image=False)
        uih = cls.objects.filter(object_id=instance.id).first()
        if not uih:
            uih = cls(object_id=instance.id)
        uih.phash = phash.__hash__()
        uih.phash_hex = str(phash)
        uih.save()

    @classmethod
    def fingerprint_interests(cls, instance, save_image=False):
        """

        :param user:
        :return:
        """
        uis = ObjectInterest.objects.filter(object_id=instance.id).all()
        width = height = 64
        im = Image.new("RGB", (width, height))
        for ui in uis:
            x, y, r, g, b = calc_pos_for_int(ui.interest_id)
            im.putpixel((x, y), (r,g,b))
        hash = imagehash.average_hash(im, hash_size=64)
        # hash = dhash(im, hash_size=64)
        if save_image:
            # this is for mostly demo purposes
            im.save("tempimages/uid_%s.jpg" % instance.id)
        return hash
