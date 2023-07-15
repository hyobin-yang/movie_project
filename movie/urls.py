from django.urls import path
from .views import *

app_name = 'movie'

urlpatterns = [
    path('', InitDBView.as_view()),
    path('list/', MovieListView.as_view(), name='movie-list'),
    path('<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('list/search/', MovieSearchView.as_view(), name='movie-search'),
    path('<int:post>/comments/', CommentDetail.as_view(), name='movie-comments'),
]