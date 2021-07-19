from django.db import models


class LinkModel(models.Model):
    url = models.URLField(max_length=255)
    text = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.text