#project/urls.py
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from .views import RegisterView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'), #book_list is the landing page for the app
    path('books/', BookListView.as_view(), name='book_list'), #book_list has URL @/books
    path("book/<int:pk>/", BookDetailView.as_view(), name="book_detail"), #book_detail has URL @/book/<PK>
    path('book/create/', BookCreateView.as_view(), name='book_create'), #book_create has URL @/book/create
    path('authors/', AuthorListView.as_view(), name='authors_list'), #authors_list has URL @/authors/
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author_detail'), #author_detail has URL @/author/<PK>
    path('quotes/', QuoteListView.as_view(), name='quotes_list'), #quotes_list has URL @/quotes
    path('rating/<int:pk>/update/', RatingUpdateView.as_view(), name='rating_update'), #rating_update has ULR @/rating/<PK>/update
    path('rating/<int:pk>/delete/', RatingDeleteView.as_view(), name='rating_delete'), #rating_delete has ULR @/rating/<PK>/delete

    path("login/", auth_views.LoginView.as_view(template_name="project/login.html"), name="Finallogin"), #app level login logic is Finallogic
    path('logout/', auth_views.LogoutView.as_view(next_page='book_list'), name='Finallogout'), #app level logout logic is Finallogout
    path('register/', RegisterView.as_view(), name='register'), #app level user registration is register
]