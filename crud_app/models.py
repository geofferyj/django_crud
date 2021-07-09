from django.db import models
from django.contrib.auth.models import User

class CRUDPost(models.Model):
    post_title = models.CharField(max_length=225, blank=False, null=False)
    post_author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    post_content = models.TextField()

    def __str__(self):
        return self.post_title
