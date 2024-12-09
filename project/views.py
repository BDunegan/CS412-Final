#project/views.py
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from django.db.models import Count
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect
from django import forms
from django.views.generic.edit import UpdateView
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import DeleteView

class RatingForm(forms.ModelForm):
    """The form used inside the book details page to rate that book"""
    class Meta:
        model = Rating
        fields = ['rating', 'review']

class QuoteForm(forms.ModelForm):
    """The form used inside the book details page to add a quote from that book"""
    class Meta:
        model = Quote
        fields = ['quote']

class BookListView(ListView):
    """The ListView representation for book_list"""
    model = Book
    template_name = 'project/book_list.html'  # Template file
    context_object_name = 'books'  # Name of the context passed to the template

    def get_queryset(self):
        """Annotate each book with its average rating."""
        return Book.objects.annotate(average_rating=Avg('rating__rating'))

class BookDetailView(DetailView):
    """The DetailView representation for book_detail"""
    model = Book
    template_name = "project/book_detail.html"
    context_object_name = "book"

    def get_success_url(self):
        """Redirect back to the book detail page."""
        return reverse('book_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """Add both forms and related data to the context."""
        context = super().get_context_data(**kwargs)
        context['quote_form'] = QuoteForm()
        context['rating_form'] = RatingForm()
        context['quotes'] = Quote.objects.filter(book=self.object)
        context['ratings'] = Rating.objects.filter(book=self.object)
        return context

    def post(self, request, *args, **kwargs):
        """Handle form submissions for both QuoteForm and RatingForm."""
        if not request.user.is_authenticated:
            # Redirect non-authenticated users to the login page
            return redirect('Finallogin')
        self.object = self.get_object()  # Fetch the book object
        if 'submit_quote' in request.POST:  # Handle QuoteForm submission
            quote_form = QuoteForm(request.POST)
            if quote_form.is_valid():
                quote = quote_form.save(commit=False)
                quote.book = self.object
                quote.save()
                return redirect(self.get_success_url())
        elif 'submit_rating' in request.POST:  # Handle RatingForm submission
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                if Rating.objects.filter(book=self.object, rating_by=self.request.user.author).exists():
                    return redirect(reverse('book_list'))  # Redirect if already rated
                rating = rating_form.save(commit=False)
                rating.book = self.object
                rating.rating_by = self.request.user.author
                rating.save()
                return redirect(self.get_success_url())
        return self.get(request, *args, **kwargs)  # Reload the page on invalid form

    
class BookCreateView(LoginRequiredMixin, CreateView):
    """The CreateView for creating a new book (An author must be logged in)"""
    model = Book
    fields = ['isbn', 'title', 'publication_date', 'theme', 'is_series', 'author']
    template_name = 'project/book_create.html'
    success_url = reverse_lazy('book_list')  # Redirect after successful form submission

    def get_login_url(self) -> str:
        """Return the URL to the login page."""
        return reverse('Finallogin')

    def get_context_data(self, **kwargs):
        """Add the logged-in user to the context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_form(self, *args, **kwargs):
        """Modify the form to include the author as a hidden field."""
        form = super().get_form(*args, **kwargs)
        # Fetch the Author associated with the logged-in user
        author = Author.objects.get(user=self.request.user)
        form.fields['author'].widget = forms.HiddenInput()
        form.initial['author'] = author.id
        return form

    def form_valid(self, form):
        """Set the author to the logged-in user's Author instance."""
        # Fetch the Author instance using the ORM
        form.instance.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)

class AuthorListView(ListView):
    """The ListView representation for author_list"""
    model = Author
    template_name = 'project/author_list.html'  # Template file
    context_object_name = 'authors'  # Name of the context passed to the template

    def get_queryset(self):
        # Annotate authors with a count of their books and filter those with at least one book
        return Author.objects.annotate(book_count=Count('book')).filter(book_count__gt=0)
    

class AuthorDetailView(DetailView):
    """The DetailView representation for author_detail"""
    model = Author
    template_name = 'project/author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        """passes the average rating for the book to context to be displayed"""
        context = super().get_context_data(**kwargs)
        # Calculate the average rating for books written by this author
        books = self.object.book_set.all()  # Fetch all books written by this author
        context['average_rating'] = books.aggregate(Avg('rating__rating'))['rating__rating__avg']
        return context

class QuoteListView(ListView):
    """The ListView representation of quote_list"""
    model = Quote
    template_name = 'project/quote_list.html'  # Template file
    context_object_name = 'quotes'  # Name of the context passed to the template

class RegisterView(CreateView):
    """Custom registration logic (so an author can be made too)"""
    form_class = UserCreationForm
    template_name = "project/register.html"
    success_url = reverse_lazy('Finallogin')  # Redirect to the login page after registration

    def get_form(self, form_class=None):
        """add the required fields to make an author to the registration form"""
        form = super().get_form(form_class)
        
        # Add additional fields to the form
        form.fields['first_name'] = forms.CharField(max_length=30, required=True, label='First Name')
        form.fields['last_name'] = forms.CharField(max_length=30, required=True, label='Last Name')
        form.fields['birth_date'] = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}), label='Birth Date')
        form.fields['region'] = forms.CharField(max_length=100, required=True, label='Region')
        
        return form

    def form_valid(self, form):
        """if a valid user is created, we make an author too!"""
        # Save the user first
        response = super().form_valid(form)
        
        # Get the created user instance
        user = self.object
        
        # Create a corresponding Author model instance for the new user using additional form data
        Author.objects.create(
            user=user,
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            birth_date=form.cleaned_data['birth_date'],
            region=form.cleaned_data['region'],
            field_or_specialty="General"  # Set a default or modify as needed
        )
        
        return response

class RatingUpdateView(LoginRequiredMixin, UpdateView):
    """Implements the Update CRUD for ratings"""
    model = Rating
    form_class = RatingForm  # Reuse the form
    template_name = "project/rating_update.html"  # Create this template for the update form

    def get_object(self, queryset=None):
        """Ensure that only the rating's author can update it."""
        obj = super().get_object(queryset)
        if obj.rating_by != self.request.user.author:
            raise PermissionDenied("You do not have permission to edit this rating.")
        return obj

    def get_success_url(self):
        """Redirect back to the book detail page."""
        return reverse('book_detail', kwargs={'pk': self.object.book.pk})
    
class RatingDeleteView(LoginRequiredMixin, DeleteView):
    """Implements the Delete CRUD for ratings"""
    model = Rating
    template_name = "project/rating_confirm_delete.html"  # Create a confirmation template

    def get_object(self, queryset=None):
        """Ensure that only the rating's author can delete it."""
        obj = super().get_object(queryset)
        if obj.rating_by != self.request.user.author:
            raise PermissionDenied("You do not have permission to delete this rating.")
        return obj

    def get_success_url(self):
        """Redirect back to the book detail page."""
        return reverse('book_detail', kwargs={'pk': self.object.book.pk})
