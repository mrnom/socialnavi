from django.contrib import admin

from posts.models import Post, Like

admin.site.register(Post, admin.ModelAdmin)
admin.site.register(Like, admin.ModelAdmin)
