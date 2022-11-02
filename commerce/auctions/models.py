from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.IntegerField()
    def __str__(self):
        return str(self.bid)



class Category(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Listing(models.Model):
    picture = models.ImageField(upload_to='auctions/files/listings_pictures', null=True, blank="True")
    title = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    followers = models.ManyToManyField(User, blank=True, related_name="followers")

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    content = models.CharField(max_length=30)
    def __str__(self):
        return self.content