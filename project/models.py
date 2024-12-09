# project/models.py
# Define the data objects for our application

from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Author(models.Model):
    '''Represents an Author. Each Author can have zero to many books and is associeated OneToOne with a User'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    birth_date = models.DateField(blank=False, default=datetime.date.today)
    death_date = models.DateField(blank=True, null=True)
    region = models.TextField(blank=False)
    field_or_specialty = models.TextField(blank=False)

    def __str__(self):
        """String representation FIRST LAST"""
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    '''Represents a Book. Each book can have many to zero quotes
    and each Author can leave one Rating per book'''
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    isbn = models.TextField(blank=False)
    title = models.TextField(blank=False)
    publication_date = models.DateField(blank=False)
    theme = models.TextField(blank=False)
    is_series = models.BooleanField(default=False)

    def __str__(self):
        """String representation TITLE"""
        return self.title
    
    def get_average_rating(self):
        """Calculates the average rating for the book across all authors using Django ORM."""
        return self.rating_set.aggregate(average=Avg('rating'))['average'] or 0


class Quote(models.Model):
    '''Represents the quotes of books'''
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quote = models.TextField(blank=False)

    def __str__(self):
        """String representation TITLE QUOTE"""
        return f"Quote for {self.book.title}: {self.quote_text[:50]}..."


class Rating(models.Model):
    '''Represents an authors rating of a book. One per author per book'''
    rating_by = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=False)
    review = models.TextField(blank=True)

    class Meta:
        """Ensures the uniqueness constraint of an author and book (one rating per author per book)"""
        unique_together = ('rating_by', 'book')  # Ensure only one review per author per book

    def __str__(self):
        """String representation TITLE AUTHOR"""
        return f"Rating for {self.book.title} by {self.rating_by}"