from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet только для чтения групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для постов. Только аутентифицированные пользователи."""

    queryset = Post.objects.all().select_related('author', 'group')
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def _get_post(self):
        """Возвращает объект поста по post_id из URL или 404."""
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)

    def get_queryset(self):
        post = self._get_post()
        return post.comments.select_related('author')

    def perform_create(self, serializer):
        post = self._get_post()
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого комментария запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого комментария запрещено!')
        super().perform_destroy(instance)
