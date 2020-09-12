from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Follow, Group, Post
from .permissions import OwnResourcePermission
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer)


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )


class GroupCreateListView(CreateListViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowCreateListView(CreateListViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, OwnResourcePermission, )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, OwnResourcePermission, )

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('id'))
        return post.comments.all()

    def perform_create(self, serializer):
        get_object_or_404(Post, id=self.kwargs.get('id'))
        serializer.save(author=self.request.user)
