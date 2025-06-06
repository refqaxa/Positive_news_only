from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class NewsArticle(models.Model):
    CATEGORY_CHOICES = [
        ('algemeen', 'Algemeen'),
        ('sport', 'Sport'),
        ('economie', 'Economie'),
    ]

    article_id = models.AutoField(primary_key=True)  # Auto-increment field
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    content = models.TextField()
    url = models.URLField(unique=True)
    image_url = models.URLField(blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    published_date = models.DateTimeField()
    sentiment_score = models.FloatField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='algemeen')

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(NewsArticle, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'article')

class Preferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    categories = models.TextField(blank=True, null=True)  # Use JSON or comma-separated values
    sources = models.TextField(blank=True, null=True)     # Use JSON or comma-separated values

    def __str__(self):
        return f"Preferences for {self.user.username}"
