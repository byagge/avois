from django.db.models import Count
from .models import Post, Tag

def get_popular_posts():
    """Возвращает популярные посты, отсортированные по количеству лайков и дате создания."""
    return Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes', '-created_at')

def get_newest_posts():
    """Возвращает новые посты, отсортированные по дате создания."""
    return Post.objects.order_by('-created_at')

def get_recommended_posts(user):
    """Возвращает рекомендованные посты для пользователя на основе его лайков."""
    user_liked_posts = Post.objects.filter(likes__user=user)
    liked_tags = Tag.objects.filter(post__in=user_liked_posts).distinct()
    recommended_posts = Post.objects.filter(tags__in=liked_tags).exclude(likes__user=user).distinct()
    return recommended_posts
