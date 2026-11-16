from django.contrib import admin

from apps.blog.models import Category, Comment, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display: tuple[str, ...] = ("id", "name", "slug")
    search_fields: tuple[str, ...] = ("name", "slug")
    prepopulated_fields: dict[str, tuple[str]] = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display: tuple[str, ...] = ("id", "name", "slug")
    search_fields: tuple[str, ...] = ("name", "slug")
    prepopulated_fields: dict[str, tuple[str]] = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display: tuple[str, ...] = (
        "id",
        "title",
        "author",
        "category",
        "status",
        "created_at",
    )
    list_filter: tuple[str, ...] = ("status", "category", "created_at")
    search_fields: tuple[str, ...] = ("title", "slug", "body", "author__email")
    prepopulated_fields: dict[str, tuple[str]] = {"slug": ("title",)}
    date_hierarchy: str = "created_at"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display: tuple[str, ...] = ("id", "post", "author", "created_at")
    list_filter: tuple[str, ...] = ("created_at",)
    search_fields: tuple[str, ...] = ("body", "author__email", "post__title")
