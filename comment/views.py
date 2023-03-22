from django.shortcuts import render

from post.permissons import IsAuthorOrAdminOrPostOwner
from . models import Comments
from rest_framework import generics, permissions
from . import serializers
# Create your views here.


class CommentCreateView(generics.CreateAPIView):
    # queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailVies(generics.RetrieveDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    #
    # def get_permissions(self):
    #     if self.request.method == 'DELETE':
    #         return IsAuthorOrAdminOrPostOwner(),
    #     return permissions.AllowAny(),
