from django.db import models

from post.models import Post


# Create your models here.
class Comments(models.Model):
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner} -> {self.post}"


    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

