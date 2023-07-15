from rest_framework import serializers
from .models import Movie, Staff, Comment

# Create your serializers here.
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model = Comment
        fields = ['post', 'user', 'created_at', 'comment']
        read_only_fields = ['user']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['name', 'role', 'image_url']

class MovieSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ['id',
            'title_kor', 
                    'title_eng',
                    'poster_url',
                    'rating_aud', 
                    'rating_cri', 
                    'rating_net',
                    'genre', 
                    'showtimes', 
                    'release_date', 
                    'rate', 
                    'summary', 
                    'staff',
                    'comments',]
