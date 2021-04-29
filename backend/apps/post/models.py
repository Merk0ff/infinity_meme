from django.db import models


class Reviewer(models.Model):
    full_name = models.CharField(max_length=100)
    user_id = models.PositiveIntegerField()
    post_tg_id = models.CharField(max_length=100)


class Channel(models.Model):
    name = models.CharField(max_length=100)
    tg_id = models.CharField(max_length=100)


class Post(models.Model):
    images = models.ManyToManyField(
        'image.Image',
    )
    reviewed_by = models.ManyToManyField(
        Reviewer,
    )
    posted_to = models.ManyToManyField(
        Channel,
    )
    reviewed_at = models.DateTimeField(null=True)
    posted_at = models.DateTimeField(null=True)
    reviewed_rating = models.PositiveIntegerField(default=0)
    on_review = models.BooleanField(default=False)
