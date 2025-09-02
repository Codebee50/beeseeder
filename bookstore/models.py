from django.db import models

# Create your models here.


from accounts.models import UserAccount
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publisher = models.CharField(max_length=255, blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True, help_text="13 Character ISBN number")
    publication_date = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='books')
    added_by = models.ForeignKey(
        UserAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='added_books',
        help_text="The user who added this book to the system."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title', 'author__name']
        unique_together = ('title', 'author') # Prevent duplicate books by the same author

    def __str__(self):
        return f"{self.title} by {self.author.name}"


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars."
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('book', 'user') # A user can only review a book once
        ordering = ['-created_at']

    def __str__(self):
        return f"Review for {self.book.title} by {self.user.username} - {self.rating} stars"




class BookLoan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    borrower = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='borrowed_books')
    checkout_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('CHECKED_OUT', 'Checked Out'),
            ('RETURNED', 'Returned'),
            ('OVERDUE', 'Overdue'),
        ],
        default='CHECKED_OUT'
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-checkout_date']

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower.username}"

