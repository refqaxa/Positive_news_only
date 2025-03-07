from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class NewsArticle(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    content = models.TextField()
    url = models.URLField(unique=True)
    image_url = models.URLField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    published_date = models.DateTimeField()
    sentiment_score = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'article')

class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    categories = models.TextField(blank=True, null=True)  # Comma-separated values
    sources = models.TextField(blank=True, null=True)     # Comma-separated values

    def __str__(self):
        return f"Preferences for {self.user.username}"
