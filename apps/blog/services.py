from django.db.models import QuerySet

from apps.blog.models import Post


def get_posts_by_author(author_id: int) -> QuerySet[Post]:
    return Post.objects.filter(author_id=author_id)
