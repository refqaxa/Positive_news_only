from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
