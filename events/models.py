from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
  """Model for event categories."""
  name = models.CharField(max_length=50, unique=True)

  def __str__(self):
    return self.name

class Event(models.Model):
  """Model for events."""
  title = models.CharField(max_length=200)
  description = models.TextField()
  date = models.DateField()
  time = models.TimeField()
  location = models.CharField(max_length=255)  # geolocations to be later
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  host = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='hosted_events')  
  group = models.ForeignKey('Group', on_delete=models.CASCADE, null=True, blank=True)

  capacity = models.PositiveIntegerField(blank=True, null=True)  # Optional
  image = models.ImageField(upload_to='events/', blank=True, null=True)  # Optional

  def __str__(self):
    return self.title

class Registration(models.Model):
  """Model for user event registrations."""
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  registered_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('user', 'event')  # Ensure a user can only register for an event once

class Group(models.Model):
  """Model for groups."""
  name = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  members = models.ManyToManyField(User, related_name='user_groups')


  def __str__(self):
    return self.name