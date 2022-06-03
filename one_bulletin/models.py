from django.db import models


# database model for a news story
class NewsStory(models.Model):
    headline = models.CharField(max_length=255)
    description = models.TextField()
    date_time = models.DateTimeField()
    link = models.TextField()
    image = models.TextField()
    sources = models.JSONField(default=list)
    relevancy = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.sources[0]}: {self.headline}"
