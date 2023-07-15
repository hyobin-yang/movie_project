from django.db import models
from members.models import CustomUser

# Create your models here.
class Movie(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    title_kor = models.CharField(max_length=30)
    title_eng = models.CharField(max_length=30)
    poster_url = models.URLField(max_length=1024)
    rating_aud = models.CharField(max_length=10)
    rating_cri = models.CharField(max_length=10)
    rating_net = models.CharField(max_length=10)
    genre = models.CharField(max_length=20)
    showtimes = models.CharField(max_length=30)
    release_date = models.CharField(max_length=30)
    rate = models.CharField(max_length=20)
    summary = models.TextField(default='')

    def __str__(self):
        return self.title_kor

class Staff(models.Model):
    movie_title = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='staff')
    name = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    image_url = models.URLField(max_length=1024)

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Movie, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return self.comment