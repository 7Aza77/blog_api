import random
import time
from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.utils.text import slugify
from faker import Faker

from apps.blog.models import Category, Comment, Post, PostStatus, Tag

User = get_user_model()

DEFAULT_USERS: int = 20
DEFAULT_POSTS: int = 100
DEFAULT_COMMENTS: int = 500
SEED_PASSWORD: str = 'password123'

PUBLISHED_RATIO: float = 0.70
NO_CATEGORY_RATIO: float = 0.10
INACTIVE_USER_RATIO: float = 0.15
STAFF_USER_RATIO: float = 0.15

MIN_TAGS_PER_POST: int = 0
MAX_TAGS_PER_POST: int = 5
POST_PARAGRAPHS_COUNT: int = 3
MIN_COMMENT_SENTENCES: int = 1
MAX_COMMENT_SENTENCES: int = 3

CATEGORIES: list[str] = [
    'Python',
    'Django',
    'DevOps',
    'Web Development',
    'Machine Learning',
    'Architecture',
    'Databases',
    'Testing',
]

TAGS: list[str] = [
    'django',
    'python',
    'postgresql',
    'docker',
    'api',
    'rest',
    'unfold',
    'orm',
    'testing',
    'celery',
    'redis',
    'fastapi',
    'git',
    'devops',
    'frontend',
    'backend',
    'security',
    'performance',
    'sql',
    'clean-code',
]


class Command(BaseCommand):
    """Management command to populate database with realistic fake data."""

    help = 'Fill the database with fake data.'

    def add_arguments(self, parser: CommandParser) -> None:
        """Register CLI arguments for seeding counts and data clearing."""
        parser.add_argument(
            '--users',
            type=int,
            default=DEFAULT_USERS,
            help='Number of users to create',
        )
        parser.add_argument(
            '--posts',
            type=int,
            default=DEFAULT_POSTS,
            help='Number of posts to create',
        )
        parser.add_argument(
            '--comments',
            type=int,
            default=DEFAULT_COMMENTS,
            help='Number of comments to create',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete existing data before seeding',
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """Execute the database seeding workflow."""
        users_count: int = options['users']
        posts_count: int = options['posts']
        comments_count: int = options['comments']
        clear: bool = options['clear']

        if users_count < 0 or posts_count < 0 or comments_count < 0:
            raise CommandError('Counts must be non-negative numbers.')

        start_time: float = time.perf_counter()
        fake: Faker = Faker()

        if clear:
            Comment.objects.all().delete()
            Post.objects.all().delete()
            Tag.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        existing_users: list[Any] = list(User.objects.all())
        if users_count == 0 and not existing_users and (posts_count > 0 or comments_count > 0):
            raise CommandError('Cannot create posts or comments without users.')

        # 1. Categories
        existing_cat_names: set[str] = set(Category.objects.values_list('name', flat=True))
        categories_to_create: list[Category] = [
            Category(name=name, slug=slugify(name))
            for name in CATEGORIES
            if name not in existing_cat_names
        ]
        if categories_to_create:
            Category.objects.bulk_create(categories_to_create)
        all_categories: list[Category] = list(Category.objects.all())

        # 2. Tags
        existing_tag_names: set[str] = set(Tag.objects.values_list('name', flat=True))
        tags_to_create: list[Tag] = [
            Tag(name=name, slug=slugify(name)) for name in TAGS if name not in existing_tag_names
        ]
        if tags_to_create:
            Tag.objects.bulk_create(tags_to_create)
        all_tags: list[Tag] = list(Tag.objects.all())

        # 3. Users
        hashed_password: str = make_password(SEED_PASSWORD)
        used_emails: set[str] = set(User.objects.values_list('email', flat=True))
        users_to_create: list[Any] = []

        for _ in range(users_count):
            first_name: str = fake.first_name()
            last_name: str = fake.last_name()
            email_base: str = f'{first_name.lower()}.{last_name.lower()}@example.com'
            email: str = email_base
            suffix: int = 1
            while email in used_emails:
                suffix += 1
                email = f'{first_name.lower()}.{last_name.lower()}{suffix}@example.com'
            used_emails.add(email)

            is_staff: bool = random.random() < STAFF_USER_RATIO
            is_active: bool = random.random() >= INACTIVE_USER_RATIO

            users_to_create.append(
                User(
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=hashed_password,
                    is_staff=is_staff,
                    is_active=is_active,
                )
            )

        created_users: list[Any] = User.objects.bulk_create(users_to_create)
        available_users: list[Any] = existing_users + created_users

        # 4. Posts
        if posts_count > 0 and not available_users:
            raise CommandError('Cannot create posts without users.')

        used_slugs: set[str] = set(Post.objects.values_list('slug', flat=True))
        posts_to_create: list[Post] = []
        post_tags_mapping: list[list[Tag]] = []

        for _ in range(posts_count):
            author = random.choice(available_users)
            title: str = fake.sentence(nb_words=6).rstrip('.')
            base_slug: str = slugify(title)
            if not base_slug:
                base_slug = f'post-{random.randint(1000, 999999)}'
            slug: str = base_slug
            suffix: int = 1
            while slug in used_slugs:
                suffix += 1
                slug = f'{base_slug}-{suffix}'
            used_slugs.add(slug)

            body: str = '\n\n'.join(fake.paragraphs(nb=POST_PARAGRAPHS_COUNT))
            category: Category | None = None
            if all_categories and random.random() >= NO_CATEGORY_RATIO:
                category = random.choice(all_categories)

            status: str = (
                PostStatus.PUBLISHED if random.random() < PUBLISHED_RATIO else PostStatus.DRAFT
            )

            posts_to_create.append(
                Post(
                    author=author,
                    title=title,
                    slug=slug,
                    body=body,
                    category=category,
                    status=status,
                )
            )

            if all_tags:
                tag_count: int = random.randint(
                    MIN_TAGS_PER_POST, min(MAX_TAGS_PER_POST, len(all_tags))
                )
                chosen_tags: list[Tag] = random.sample(all_tags, tag_count)
            else:
                chosen_tags = []
            post_tags_mapping.append(chosen_tags)

        created_posts: list[Post] = Post.objects.bulk_create(posts_to_create)
        for post, tags in zip(created_posts, post_tags_mapping, strict=False):
            if tags:
                post.tags.set(tags)

        # 5. Comments
        published_posts: list[Post] = list(Post.objects.filter(status=PostStatus.PUBLISHED))
        if comments_count > 0 and not published_posts:
            raise CommandError('Cannot create comments because there are no published posts.')

        comments_to_create: list[Comment] = []
        if published_posts and available_users:
            for _ in range(comments_count):
                post = random.choice(published_posts)
                author = random.choice(available_users)
                sentence_count: int = random.randint(MIN_COMMENT_SENTENCES, MAX_COMMENT_SENTENCES)
                body: str = ' '.join(fake.sentences(nb=sentence_count))

                comments_to_create.append(
                    Comment(
                        post=post,
                        author=author,
                        body=body,
                    )
                )

        Comment.objects.bulk_create(comments_to_create)

        elapsed: float = time.perf_counter() - start_time

        self.stdout.write(self.style.SUCCESS(f'Users:       {len(created_users):>5} created'))
        self.stdout.write(
            self.style.SUCCESS(f'Categories:  {len(categories_to_create):>5} created')
        )
        self.stdout.write(self.style.SUCCESS(f'Tags:        {len(tags_to_create):>5} created'))
        self.stdout.write(self.style.SUCCESS(f'Posts:       {len(created_posts):>5} created'))
        self.stdout.write(self.style.SUCCESS(f'Comments:    {len(comments_to_create):>5} created'))
        self.stdout.write(self.style.SUCCESS(f'Done in {elapsed:.2f} seconds'))

