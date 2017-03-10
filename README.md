recomserver
===========

A generic recommendation, similarity server built with perceptual hashing and hamming distance.

Wait what ? 

For detailed description of what a perceptual hash is please read, http://blog.iconfinder.com/detecting-duplicate-images-using-python/

For a very very short description, for image similarity we generate a fingerprint for each image, then calculate the distance between them. If they are
close to each other, then we can say they are the same, or very likely to be the same.

So the main idea is, what if we generate an image based on the interest data, and calculate similarity between two interests.

Please note that this project is EXPERIMENTAL, well you are warned.

For example,
------------

The classical way of recommending users to follow.

We create a tags table, where you insert each of the tags and we create another table to relate users to tags, user_tags.

User A, likes reading articles tagged with Spiderman, Flintstones, Fusion Jazz, Cartoons
User B, likes reading articles tagged with Sci-fy, Flintstones, Inanimate objects, Cartoons
User C, likes reading articles tagged with Time Machines, Mobile phones, Telegraphs, Minimalism, Cartoons


```
Tags:
id  | name
----| ------
1   | Spiderman
2   | Flintstones
3   | Fusion Jazz
4   | Cartoons
5   | Sci-fy
6   | Inanimate objects
7   | Time Machines
8   | Mobile phones
9   | Telegraphs
10  | Minimalism
```



```
UserTags:
id  | user_id | tag_id
----| --------|--------
1   | 1       | 1
2   | 1       | 2
3   | 1       | 3
4   | 1       | 4
5   | 2       | 5
6   | 2       | 2
7   | 2       | 6
8   | 2       | 4
9   | 3       | 7    
10  | 3       | 8
11  | 3       | 9
12  | 3       | 10
13  | 3       | 4
```

then suppose you want to recommend users to user A, based on common interests, all you need to do is, to make a simple query like

```
select user_id, (
             select count(tag_id)
             from user_tags
             where user_id=UT.user_id
             and tag_id in (select tag_id from user_tags where user_id=1)
         ) as common_tags_count
 from user_tags UT
 order by common_tags_count desc limit 5;
```

this should supposedly output something like this

```
user_id | common_tags_count
---------------------------
1       | 4
2       | 2
3       | 1
```

So you pick the second second user and you are good to go.

This goes works well and you go live.

But the question is what happens if you have more than a few thousand users with hundreds of content tags. 
You'll quickly realize that your query takes ages, your database servers gets down to their knees and you start looking for
alternatives.

So this is an alternative attack for that problem - or you can go with spark, hadoop, graph databases or whatever and enjoy the added complexity,
or you can write a simple server with scipy and others and calculate KNN (or an alternative) where you might enjoy playing with it. 

If you are still reading, here is what we do.

We generate a one dimensional array from user_tags

```
user A => (1,2,3,4)
user B => (5,2,6,4)
user C => (7,8,9,10,4)
```

then we convert it to 3d (x, y position and color code) and plot to an image

the images becomes like, (of course there are more than a few datapoints on these images)

![uid_1](sampleimages/uid_1.jpg "uid_1")
![uid_2](sampleimages/uid_1.jpg "uid_2")
![uid_3](sampleimages/uid_1.jpg "uid_3")

then we calculate a perceptual hash and store in a table.

which becomes like

```
user_tags_hash

user_id | hash
------------------
| 1     |  5321 |
| 2     |  6183 |
| 3     |  4781 |
```

and then we calculate the hamming distance and sort by it with a simple query

```
select user_id,
         BIT_COUNT(phash ^ (select phash from user_tags_hash where user_id=1)) as hd
from user_tags_hash
order by hd asc limit 5
```

which is supposed to give something like

```
user_id | hd
---------------------------
1       | 0
2       | 1
3       | 2
```

this of course does a table scan, since it can't use an index, but still it does a binary operation on a relatively small subset, so its pretty fast.

to give you some non scientific benchmarks, for example for 10000 users with 200 tags, humming distance query returns under 0.01 and 
query for finding similar counts doesn't complete after a few minutes.


Installation
--------------

This is a simple django-rest-framework project. Simply cloning the repo, installing the requirements should make it work.

```
git clone ...
cd recomserver
virtualenv env
source env/bin/activate
pip install -U pip
pip install -r requirements/local.txt
```

then edit config/settings/base.py to create your db

```
python manage.py migrate
```

and now you can run your server

```
python manage.py runserver
```

of course there is no data, to play around you can create some

```
python create_demo.py
```

and then you can get matches

```
http localhost:8000/api/interests/similar/3/?limit=10
```


Notes & Remarks
------------------
0. this project is not intended for production use but to serve as an example ,
i. If you have a small set of this will give you unexpected results, but maybe its better to use 
ii. this only works with MySQL right now, probably implementing in postgresql with some extension and using
gist indexes will result in much faster results.

License
---------
MIT


