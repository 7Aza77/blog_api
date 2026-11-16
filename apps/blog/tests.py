from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from apps.blog.models import Category, Comment, Post, PostStatus, Tag
from apps.blog.services import get_posts_by_author

User = get_user_model()


class BlogModelTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="writer@example.com",
            password="password123",
            first_name="Jane",
            last_name="Doe",
        )
        self.category = Category.objects.create(
            name="Technology",
            slug="technology",
        )
        self.tag_python = Tag.objects.create(
            name="Python",
            slug="python",
        )
        self.tag_django = Tag.objects.create(
            name="Django",
            slug="django",
        )

    def test_category_creation_and_string_representation(self) -> None:
        self.assertEqual(str(self.category), "Technology")
        self.assertEqual(self.category.slug, "technology")

    def test_category_unique_name(self) -> None:
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Technology", slug="tech-2")

    def test_tag_creation_and_string_representation(self) -> None:
        self.assertEqual(str(self.tag_python), "Python")
        self.assertEqual(self.tag_python.slug, "python")

    def test_tag_unique_name(self) -> None:
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name="Python", slug="python-2")

    def test_post_creation_with_tags_and_category(self) -> None:
        post = Post.objects.create(
            author=self.user,
            title="Building REST APIs with Django",
            slug="building-rest-apis-with-django",
            body="Comprehensive guide to Django REST Framework architecture.",
            category=self.category,
            status=PostStatus.PUBLISHED,
        )
        post.tags.set([self.tag_python, self.tag_django])

        self.assertEqual(str(post), "Building REST APIs with Django")
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.category, self.category)
        self.assertEqual(post.status, PostStatus.PUBLISHED)
        self.assertEqual(post.tags.count(), 2)
        self.assertIsNotNone(post.created_at)
        self.assertIsNotNone(post.updated_at)

    def test_comment_creation(self) -> None:
        post = Post.objects.create(
            author=self.user,
            title="Clean Architecture",
            slug="clean-architecture",
            body="Article body content.",
            category=self.category,
            status=PostStatus.PUBLISHED,
        )
        comment = Comment.objects.create(
            post=post,
            author=self.user,
            body="Great article!",
        )

        self.assertEqual(comment.post, post)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.body, "Great article!")
        self.assertIn("Comment by", str(comment))
        self.assertIsNotNone(comment.created_at)

    def test_get_posts_by_author_service(self) -> None:
        post = Post.objects.create(
            author=self.user,
            title="First Post",
            slug="first-post",
            body="Hello World",
            category=self.category,
            status=PostStatus.PUBLISHED,
        )
        author_posts = get_posts_by_author(self.user.id)
        self.assertEqual(list(author_posts), [post])
