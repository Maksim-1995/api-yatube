from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from posts.models import Post, Group, Comment
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
        """При создании поста автоматически устанавливаем автора."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=('get', 'post'), url_path='comments')
    def comments(self, request, pk=None):
        """Список комментариев к посту или создание нового."""
        post = self.get_object()
        if request.method == 'GET':
            comments = post.comments.select_related('author')
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=('get', 'put', 'patch', 'delete'),
        url_path=r'comments/(?P<comment_id>\d+)'
    )
    def comment_detail(self, request, pk=None, comment_id=None):
        """Получение, изменение или удаление конкретного комментария."""
        post = self.get_object()
        comment = get_object_or_404(Comment, pk=comment_id, post=post)
        if request.method == 'GET':
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        self.check_object_permissions(request, comment)
        if request.method in ('PUT', 'PATCH'):
            serializer = CommentSerializer(
                comment,
                data=request.data,
                partial=(request.method == 'PATCH')
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
