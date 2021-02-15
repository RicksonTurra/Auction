from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class commentsListing(models.Model):
    comments = models.CharField(max_length=200, default="no comments yet.")
    
    def __str__(self):
        return f"{self.comments}"

class AuctListing(models.Model):
    title = models.CharField(max_length=64, default='Product')
    description = models.CharField(max_length=200, default='Description')
    starting_bid = models.IntegerField(default=0)
    user_name = models.CharField(max_length=64, default='Anonymous')
    comments_title = models.ManyToManyField(commentsListing, related_name="comment_comment")

    def __str__(self):
        return f"{self.title}: {self.description} price: {self.starting_bid}"
class bidsListing(models.Model):
    pass



class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        ordering = ['headline']

    def __str__(self):
        return self.headline


