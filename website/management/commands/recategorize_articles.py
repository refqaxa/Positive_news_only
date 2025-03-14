from django.core.management.base import BaseCommand
from website.models import NewsArticle
from website.services import determine_category

class Command(BaseCommand):
    help = 'Recategorize all existing articles using the updated category logic'

    def handle(self, *args, **options):
        articles = NewsArticle.objects.all()
        total = articles.count()
        updated = 0

        self.stdout.write(f"Found {total} articles to process...")

        for article in articles:
            old_category = article.category
            new_category = determine_category(article.title, article.description)
            
            if old_category != new_category:
                article.category = new_category
                article.save()
                updated += 1
                self.stdout.write(f"Updated article '{article.title}' from {old_category} to {new_category}")

        self.stdout.write(self.style.SUCCESS(f"Successfully recategorized {updated} articles out of {total}")) 