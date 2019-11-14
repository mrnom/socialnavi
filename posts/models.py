from django.db import models
from accounts.models import User


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts',
                               on_delete=models.CASCADE)

    title = models.CharField(max_length=100)

    text = models.TextField(blank=True)

    created = models.DateTimeField(auto_now_add=True)

    edited = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(User, blank=True, through='Like',
                                   through_fields=('post', 'user'))

    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return 'User {} likes the post: {}'.format(self.user, self.post)