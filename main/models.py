# import uuid
# from django.db import models



# class ReddApiKey(models.Model):
#     """
#     Model to store and manage API keys for users.
#     """
#     # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
#     key = models.CharField(max_length=32, unique=True, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)

#     def save(self, *args, **kwargs):
#         """
#         Generates a unique API key before saving a new instance.
#         """
#         if not self.key:
#             self.key = uuid.uuid4().hex
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"API Key for {self.user.name}"
