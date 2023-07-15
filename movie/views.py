from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Count
from .models import Movie, Staff, Comment
from .serializers import MovieSerializer, StaffSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
import requests
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from members.models import CustomUser
from rest_framework.generics import ListCreateAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
class InitDBView(APIView):
    def get(self, request):
        url = "https://api.hufs-likelion-movie.kro.kr/movies"
        res = requests.get(url)
        movies = res.json()['movies']
        
        for movie in movies:
            movie_data = Movie()
            movie_data.title_kor = movie['title_kor']
            movie_data.title_eng = movie['title_eng']
            movie_data.poster_url = movie['poster_url']
            movie_data.rating_aud = movie['rating_aud']
            movie_data.rating_cri = movie['rating_cri']
            movie_data.rating_net = movie['rating_net']
            movie_data.genre = movie['genre']
            movie_data.showtimes = movie['showtimes']
            movie_data.release_date = movie['release_date']
            movie_data.rate = movie['rate']
            movie_data.summary = movie['summary']
            movie_data.save()

            for staff in movie['staff']:
                staff_data = Staff()
                staff_data.movie_title = movie_data
                staff_data.name = staff['name']
                staff_data.role = staff['role']
                staff_data.image_url = staff['image_url']
                staff_data.save()
        
        duplicated_names = Movie.objects.values('title_kor').annotate(name_count=Count('title_kor')).filter(name_count__gt=1)
        for title in duplicated_names:
            duplicates = Movie.objects.filter(title_kor=title['title_kor'])
            duplicates.exclude(pk=duplicates.first().pk).delete()

        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
        # return redirect(reverse('movie:movie-list'))

class MoviePagination(LimitOffsetPagination):
    default_limit = 10

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    pagination_class = MoviePagination
    # serializer_class = MovieSerializer
    def get_serializer_class(self):
        # 'title_kor'와 'poster_url'만 반환하는 커스텀 Serializer 클래스 생성
        class CustomMovieSerializer(MovieSerializer):
            class Meta(MovieSerializer.Meta):
                fields = ('title_kor', 'poster_url')
        return CustomMovieSerializer
    
class MovieDetailView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieSearchView(generics.ListAPIView):
    serializer_class = MovieSerializer
    def get_queryset(self):
        queryset = Movie.objects.all()
        title_kor = self.request.query_params.get('title_kor', None)
        if title_kor is not None:
            queryset = queryset.filter(title_kor__icontains=title_kor)
        return queryset


class CommentDetail(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post']
        return Comment.objects.filter(post=post_id)

    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = user)



