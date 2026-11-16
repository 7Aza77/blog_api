from django.http import HttpRequest

from apps.blog.models import Post, PostStatus
from settings import conf


def environment_callback(request: HttpRequest) -> list[str]:
    """Return environment badge text and style color for Unfold navigation."""
    if conf.ENV_ID == 'local':
        return ['Local', 'warning']
    return ['Production', 'danger']


def drafts_badge(request: HttpRequest) -> int:
    """Return number of draft posts for display on Posts sidebar item."""
    return Post.objects.filter(status=PostStatus.DRAFT).count()


# TODO(hw2): dashboard callback function to supply statistics context for admin index
# TODO(hw2): dashboard cards component for total users, published posts, drafts, and comments
# TODO(hw2): dashboard bar chart component for number of posts per category
# TODO(hw2): dashboard table component displaying top 5 authors by number of posts
# TODO(hw2): dashboard progress bars component for share of published vs draft posts
