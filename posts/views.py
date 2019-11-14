from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import Post, Like
from posts.permissions import IsAuthorOrReadOnly
from posts.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post', 'delete'], detail=True)
    def like(self, request, pk=None):
        post = Post.objects.get(id=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        serializer = self.get_serializer(post)

        if not like and request.method == 'POST':
            Like.objects.create(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif like and request.method == 'DELETE':
            like.delete()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.data, status=status.HTTP_200_OK)
