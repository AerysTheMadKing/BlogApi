# from django.shortcuts import render
# from rest_framework import generics
# from rest_framework import permissions
#
# from . import serializers
# from post.models import Post
# from .permissons import IsAuthorOrAdmin, IsAuthor
#
#
from rest_framework import permissions, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter # Для поиска
from django_filters.rest_framework import DjangoFilterBackend


from like.models import Favorites
from like.serializers import LikedUsersSerializer
from post import serializers
from post.models import Post
from .permissons import IsAuthorOrAdmin, IsAuthor


class StandartResultPagination(PageNumberPagination):
    page_size = 1
    page_query_param = 'page'


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title',)
    filterset_fields = ('owner', 'category')


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializers

        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateSerializers

        return serializers.PostDetailSerializers

    def get_permissions(self):
        # удалять может админ или автор поста
        if self.action == 'destroy':
            return [permissions.IsAuthenticated(),
                    IsAuthorOrAdmin()]
        # обновлять может только автор поста
        elif self.action in ('update', 'partial_update'):
            return [permissions.IsAuthenticated(),
                    IsAuthor()]
        # просматривать могут все но создавать только залогиненный автор
        return [permissions.IsAuthenticatedOrReadOnly()]


    # ...api/v1/posts/<id>/comments/
    @action(['GET'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comments = post.comments.all()
        serializer = serializers.CommentSerializer(instance=comments, many=True)
        return Response(serializer.data, status=200)

    @action(['GET'], detail=True)
    def likes(self, request, pk):
        post = self.get_object()
        likes = post.likes.all()
        serializer = LikedUsersSerializer(instance=likes, many=True)
        return Response(serializer.data, status=200)

    # .../api/v1/posts/<12>/favorites/
    @action(['POST', 'DELETE'], detail=True)
    def favorites(self, request, pk):
        post = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.favorites.filter(post=post).exists():
                return Response('This post is already in favorites!', status=400)
            Favorites.objects.create(owner=user, post=post)
            return Response('Added to favorites!', status=201)

        else:
            favorite = user.favorites.filter(post=post)
            if favorite.exists():
                favorite.delete()
                return Response('Deleted from favorites!', status=204)
            return Response('Post not found!', status=404)








class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PostListSerializers
        return serializers.PostCreateSerializers


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return serializers.PostCreateSerializers
        return serializers.PostDetailSerializers

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return IsAuthorOrAdmin(),
        elif self.request.method in ('PUT', 'PATCH'):
            return IsAuthor(),
        return permissions.AllowAny(),
#



