from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    """A subject the user is learning about."""
    text = models.CharField(max_length=300)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Returns a string representation of the model."""
        return self.text


class Entry(models.Model):
    """Something specific learned about a subject."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        """Returns a string representation of the model."""
        return self.text[:50] + '...'
