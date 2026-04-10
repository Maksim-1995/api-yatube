from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet только для чтения групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для постов. Только аутентифицированные пользователи."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """При создании поста автоматически устанавливаем автора."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Запрещаем редактирование чужого поста."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Запрещаем удаление чужого поста."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев. Только аутентифицированные пользователи."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Возвращаем комментарии только для конкретного поста."""
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(
            post__id=post_id).select_related('author')

    def perform_create(self, serializer):
        """При создании комментария автоматически устанавливаем автора."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        """Запрещаем редактирование чужого комментария."""
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """Запрещаем удаление чужого комментария."""
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()
