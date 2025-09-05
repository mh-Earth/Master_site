from django.db import models
import json

class RedditAdmin(models.Model):
    """
    Model for an admin user.
    """
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255) # NOTE: Storing plain passwords is insecure. Use Django's built-in authentication system for production.

    def __str__(self):
        return self.username

class RedditAdminPlaneUrls(models.Model):
    """
    Model for a temporary admin panel URL with a slug.
    """
    slug = models.CharField(max_length=64, unique=True)
    create_at = models.FloatField()
    live = models.IntegerField(default=600)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return self.slug

    def to_json(self):
        """
        Helper method to convert model instance to a JSON-serializable dictionary.
        """
        return {
            'slug': self.slug,
            'create_at': self.create_at,
            'live': self.live,
            'expired': self.expired,
        }

class RedditSubmission(models.Model):
    """
    Model for a Reddit submission.
    """
    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    # Using JSONField for tags to store a list of strings
    tags = models.JSONField(default=list)

    def __str__(self):
        return self.name

    def to_json(self):
        """
        Helper method to convert model instance to a JSON-serializable dictionary.
        """
        return {
            'name': self.name,
            'title': self.title,
            'tags': self.tags,
        }

class RedditPosted(models.Model):
    """
    Model for submissions that have been posted.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
        
    def to_json(self):
        """
        Helper method to convert model instance to a JSON-serializable dictionary.
        """
        return {
            'name': self.name
        }

class RedditSettings(models.Model):
    """
    Model to store application settings.
    """
    limit = models.IntegerField(default=50)
    mode = models.CharField(max_length=50, default='day')
    is_reversed = models.BooleanField(default=True)

    def __str__(self):
        return f"Settings (limit: {self.limit}, mode: {self.mode})"

    def to_json(self):
        """
        Helper method to convert model instance to a JSON-serializable dictionary.
        """
        return {
            'limit': self.limit,
            'mode': self.mode,
            'is_reversed': self.is_reversed,
        }
# class 