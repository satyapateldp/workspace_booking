from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    age = models.PositiveIntegerField(default=18)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    

class Room(models.Model):
    ROOM_TYPES = [
        ("PRIVATE", "Private"),
        ("CONFERENCE", "Conference"),
        ("SHARED", "Shared Desk"),
    ]
    name = models.CharField(max_length=50)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class Team(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="teams")

    def __str__(self):
        return self.name
    
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    slot = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room.name} - {self.slot}"
