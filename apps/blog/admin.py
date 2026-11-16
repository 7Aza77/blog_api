from django.contrib import admin
from django.db.models import Count, QuerySet
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import AutocompleteSelectFilter, RangeDateTimeFilter
from unfold.decorators import display
from unfold.sections import TableSection

from apps.blog.constants import COMMENT_BODY_TRUNCATE_LENGTH
from apps.blog.models import Category, Comment, Post, Tag


class CategoryPostSection(TableSection):
    """Expandable row section showing category posts in a table."""

    verbose_name = 'Posts'
    related_name = 'posts'
    fields = ['title', 'author', 'status', 'created_at']


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    """Category model admin configured for Unfold."""

    list_display = ('name', 'slug', 'show_posts_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_sections = [CategoryPostSection]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Category]:
        """Annotate categories with total related posts count."""
        return super().get_queryset(request).annotate(posts_count=Count('posts'))

    @display(description='Posts', ordering='posts_count')
    def show_posts_count(self, obj: Category) -> int:
        """Display sortable posts count column."""
        return getattr(obj, 'posts_count', 0)


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    """Tag model admin configured for Unfold."""

    list_display = ('name', 'slug', 'show_posts_count')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def get_queryset(self, request: HttpRequest) -> QuerySet[Tag]:
        """Annotate tags with total related posts count."""
        return super().get_queryset(request).annotate(posts_count=Count('posts'))

    @display(description='Posts', ordering='posts_count')
    def show_posts_count(self, obj: Tag) -> int:
        """Display sortable posts count column."""
        return getattr(obj, 'posts_count', 0)


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    """Comment model admin configured for Unfold with autocomplete filters."""

    list_display = ('post_title', 'author', 'short_body', 'created_at')
    list_filter = [
        ('post', AutocompleteSelectFilter),
        ('author', AutocompleteSelectFilter),
        ('created_at', RangeDateTimeFilter),
    ]
    list_filter_submit = True
    search_fields = ('body', 'author__email', 'post__title')
    autocomplete_fields = ('post', 'author')
    list_select_related = ('post', 'author')

    @display(description='Post', ordering='post__title')
    def post_title(self, obj: Comment) -> str:
        """Display title of the commented post."""
        return obj.post.title

    @display(description='Body')
    def short_body(self, obj: Comment) -> str:
        """Display shortened body text limited to constant length."""
        if len(obj.body) > COMMENT_BODY_TRUNCATE_LENGTH:
            return f'{obj.body[:COMMENT_BODY_TRUNCATE_LENGTH]}...'
        return obj.body


@admin.register(Post)
class PostAdmin(ModelAdmin):
    """Post model admin stub for Unfold with TODO markers for remaining features."""

    list_display = ('title', 'author', 'status', 'created_at')
    search_fields = ('title',)

    # TODO(hw2): header column displaying title and author
    # TODO(hw2): colored status label (published green, draft orange)
    # TODO(hw2): category dropdown column in changelist
    # TODO(hw2): tags dropdown column in changelist
    # TODO(hw2): sortable comments count column with annotate
    # TODO(hw2): status dropdown filter in changelist
    # TODO(hw2): category dropdown filter in changelist
    # TODO(hw2): tags multiple choice filter in changelist
    # TODO(hw2): author autocomplete filter in changelist
    # TODO(hw2): created_at date range filter in changelist
    # TODO(hw2): list_filter_submit button for filters
    # TODO(hw2): search by body and author email
    # TODO(hw2): expandable row showing comments of the post via list_sections
    # TODO(hw2): select_related and prefetch_related optimization to eliminate N+1 queries
    # TODO(hw2): bulk actions to publish selected posts and move to drafts
    # TODO(hw2): row action to publish or unpublish individual post
    # TODO(hw2): list action above list to publish all drafts
    # TODO(hw2): detail action on post page to open comments
    # TODO(hw2): submit-line action to save and publish post
    # TODO(hw2): tabbed edit form with Content, Classification, and Meta tabs
    # TODO(hw2): prepopulated slug field from title
    # TODO(hw2): autocomplete fields for author, category, and tags in form
    # TODO(hw2): WYSIWYG editor widget for post body field
    # TODO(hw2): read-only created_at and updated_at date fields in edit form
    # TODO(hw2): warn_unsaved_form enabled on edit form
    # TODO(hw2): comments inline displayed in its own tab with 10 per page


