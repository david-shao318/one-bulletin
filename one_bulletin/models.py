from django.db import models


class NewsStory(models.Model):
    headline = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    sources = models.JSONField(default=list)
    relevancy = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.sources[0]}: {self.headline}"
