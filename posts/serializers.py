from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='posts-detail')
    author = serializers.ReadOnlyField(source='author.id')
    likes = serializers.IntegerField(source='likes_count', required=False)

    class Meta:
        model = Post
        fields = ['url', 'id', 'author', 'title', 'text', 'created', 'edited',
                  'likes']
