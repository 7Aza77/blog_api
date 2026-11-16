from datetime import timedelta
from typing import Any

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db import connection
from django.db.models import QuerySet
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

from apps.blog import queries
from apps.blog.models import Post, PostStatus

PREVIEW_ROWS: int = 5
MUTATING_QUERIES: set[int] = {40, 41, 42, 43, 44}

def get_sample_arguments() -> dict[int, dict[str, Any]]:
    today = timezone.now()
    post = Post.objects.first()
    author_email = (
        Post.objects.filter(status=PostStatus.PUBLISHED)
        .values_list('author__email', flat=True)
        .first()
    )
    word = post.title.split()[0] if post else ''

    return {
        4: {'slug': post.slug if post else ''},
        7: {'page': 2},
        8: {'word': word},
        9: {'domain': 'example.com'},
        11: {'slugs': ['django', 'python']},
        12: {'year': today.year, 'month': today.month},
        13: {'days': 30},
        14: {'start': (today - timedelta(days=60)).date(), 'end': today.date()},
        15: {'email': author_email or ''},
        16: {'tag_slug': 'python'},
        17: {'category_slug': 'django'},
        21: {'first_slug': 'python', 'second_slug': 'django'},
        22: {'text': word},
        34: {'min_posts': 3},
        40: {'name': 'Django ORM'},
        41: {'days': 30},
        42: {'category_slug': 'django', 'tag_slug': 'orm'},
        43: {'source_slug': 'testing', 'target_slug': 'architecture'},
    }

class Command(BaseCommand):

    help = 'Run ORM queries.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--number', type=int, help='Запустить только этот запрос')
        parser.add_argument('--sql', action='store_true', help='Показать SQL')

    def handle(self, *args: Any, **options: Any) -> None:
        number: int | None = options['number']

        if number is None:

            numbers = [n for n in sorted(queries.QUERIES) if n not in MUTATING_QUERIES]
        elif number in queries.QUERIES:
            numbers = [number]
        else:
            raise CommandError(f'Query #{number} does not exist.')

        arguments = get_sample_arguments()
        for n in numbers:
            self.run_one(n, arguments.get(n, {}), options['sql'])

    def run_one(self, number: int, kwargs: dict[str, Any], show_sql: bool) -> None:
        function = queries.QUERIES[number]
        extra_fields: list[str] = []

        with CaptureQueriesContext(connection) as context:
            result = function(**kwargs)
            if isinstance(result, QuerySet):
                extra_fields = list(result.query.annotations)
                result = list(result)

        sql_count: int = len(context.captured_queries)
        self.stdout.write(self.style.MIGRATE_HEADING(
            f'#{number} {function.__name__} — {sql_count} SQL query'
        ))

        if show_sql:
            for item in context.captured_queries:
                self.stdout.write(item['sql'])

        if isinstance(result, list):
            for row in result[:PREVIEW_ROWS]:
                extras = {name: getattr(row, name) for name in extra_fields}
                self.stdout.write(f'  {row} {extras}' if extras else f'  {row}')
            self.stdout.write(f'  ({len(result)} rows)')
        else:
            self.stdout.write(f'  {result}')

