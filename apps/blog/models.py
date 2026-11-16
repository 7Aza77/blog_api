from django.conf import settings
from django.db import models

from apps.blog.constants import (
    CATEGORY_NAME_MAX_LENGTH,
    CATEGORY_SLUG_MAX_LENGTH,
    POST_SLUG_MAX_LENGTH,
    POST_STATUS_MAX_LENGTH,
    POST_TITLE_MAX_LENGTH,
    TAG_NAME_MAX_LENGTH,
    TAG_SLUG_MAX_LENGTH,
)


class PostStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"


class Category(models.Model):
    name: models.CharField = models.CharField(
        max_length=CATEGORY_NAME_MAX_LENGTH,
        unique=True,
        verbose_name="name",
    )
    slug: models.SlugField = models.SlugField(
        max_length=CATEGORY_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name="slug",
    )

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name: models.CharField = models.CharField(
        max_length=TAG_NAME_MAX_LENGTH,
        unique=True,
        verbose_name="name",
    )
    slug: models.SlugField = models.SlugField(
        max_length=TAG_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name="slug",
    )

    class Meta:
        verbose_name = "tag"
        verbose_name_plural = "tags"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    author: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="author",
    )
    title: models.CharField = models.CharField(
        max_length=POST_TITLE_MAX_LENGTH,
        verbose_name="title",
    )
    slug: models.SlugField = models.SlugField(
        max_length=POST_SLUG_MAX_LENGTH,
        unique=True,
        verbose_name="slug",
    )
    body: models.TextField = models.TextField(
        verbose_name="body",
    )
    category: models.ForeignKey = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="category",
    )
    tags: models.ManyToManyField = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="posts",
        verbose_name="tags",
    )
    status: models.CharField = models.CharField(
        max_length=POST_STATUS_MAX_LENGTH,
        choices=PostStatus.choices,
        default=PostStatus.DRAFT,
        verbose_name="status",
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="created at",
    )
    updated_at: models.DateTimeField = models.DateTimeField(
        auto_now=True,
        verbose_name="updated at",
    )

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    post: models.ForeignKey = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="post",
    )
    author: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="author",
    )
    body: models.TextField = models.TextField(
        verbose_name="body",
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="created at",
    )

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Comment by {self.author} on {self.post}"


def get_posts_by_author(author_id: int) -> models.QuerySet[Post]:
    return Post.objects.filter(author_id=author_id)
