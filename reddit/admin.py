from django.contrib import admin
from .models import RedditAdmin,RedditAdminPlaneUrls,RedditPosted,RedditSettings,RedditSubmission
# Register your models here.
admin.site.register([RedditAdmin,RedditAdminPlaneUrls,RedditPosted,RedditSettings,RedditSubmission])