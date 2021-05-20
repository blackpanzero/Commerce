from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    pass



    
class Listing(models.Model):
    CATEGORIES = (
    ('LAP', 'Laptop'),
    ('CON', 'Console'),
    ('GAD', 'Gadget'),
    ('GAM', 'Game'),
    ('TEL', 'TV')
    )

    title=models.CharField(max_length=64)
    photo=models.CharField(max_length=255)
    description=models.CharField(max_length=255,default="" )
    date=models.DateTimeField()
    categories=models.CharField(max_length=64,default="",choices=CATEGORIES)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,default="",related_name="listings")
    status=models.CharField(max_length=32,default="active")
    price=models.IntegerField(default=0)
    

    

    def __str__(self): 
        return f"{self.title}:{self.photo} to {self.date}"

class comments(models.Model):
    comments=models.CharField(max_length=255)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,)
    listing_id=models.ForeignKey(Listing,on_delete=models.CASCADE)
    date=models.DateTimeField(default=datetime.datetime.now)
    

class Bids(models.Model):
    Bid=models.IntegerField()
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,default=0,related_name="bid")
    user=models.ForeignKey(User,on_delete=models.CASCADE,default="",related_name="bids")

class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self): 
     return f"{self.user_id}:{self.listing_id} "