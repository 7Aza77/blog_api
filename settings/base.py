from pathlib import Path

from django.urls import reverse_lazy

from settings import conf

BASE_DIR: Path = conf.BASE_DIR
SECRET_KEY: str = conf.SECRET_KEY
ALLOWED_HOSTS: list[str] = conf.ALLOWED_HOSTS

INSTALLED_APPS: list[str] = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.auths',
    'apps.blog',
]

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF: str = 'settings.urls'

TEMPLATES: list[dict] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION: str = 'settings.wsgi.application'
ASGI_APPLICATION: str = 'settings.asgi.application'

AUTH_USER_MODEL: str = 'auths.User'

AUTH_PASSWORD_VALIDATORS: list[dict] = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE: str = 'en-us'
TIME_ZONE: str = 'UTC'
USE_I18N: bool = True
USE_TZ: bool = True

STATIC_URL: str = 'static/'
STATIC_ROOT: Path = BASE_DIR / 'staticfiles'

MEDIA_URL: str = 'media/'
MEDIA_ROOT: Path = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'

LOGS_DIR: Path = BASE_DIR / 'logs'
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOGGING: dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': str(LOGS_DIR / 'blog_api.log'),
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

UNFOLD: dict = {
    'SITE_TITLE': 'Blog API Admin',
    'SITE_HEADER': 'Blog API Administration',
    'SITE_SUBHEADER': 'Content & Community Management',
    'SITE_SYMBOL': 'article',
    'COLORS': {
        'primary': {
            '50': 'oklch(97.9% .021 166.113)',
            '100': 'oklch(95% .052 163.051)',
            '200': 'oklch(90.5% .093 164.15)',
            '300': 'oklch(84.5% .143 164.978)',
            '400': 'oklch(76.5% .177 163.223)',
            '500': 'oklch(69.6% .17 162.48)',
            '600': 'oklch(59.6% .145 163.225)',
            '700': 'oklch(50.8% .118 165.612)',
            '800': 'oklch(43.2% .095 166.913)',
            '900': 'oklch(37.8% .077 168.94)',
            '950': 'oklch(26.2% .051 172.552)',
        },
    },
    'ENVIRONMENT': 'apps.blog.callbacks.environment_callback',
    'SITE_DROPDOWN': [
        {
            'icon': 'code',
            'title': 'GitHub Repository',
            'link': 'https://github.com/7Aza77/blog_api',
        },
        {
            'icon': 'menu_book',
            'title': 'Unfold Documentation',
            'link': 'https://unfoldadmin.com/docs/',
        },
    ],
    'COMMAND': {
        'search_models': True,
    },
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': False,
        'navigation': [
            {
                'title': 'Overview',
                'items': [
                    {
                        'title': 'Dashboard',
                        'icon': 'dashboard',
                        'link': reverse_lazy('admin:index'),
                    },
                ],
            },
            {
                'title': 'Content',
                'items': [
                    {
                        'title': 'Posts',
                        'icon': 'article',
                        'link': reverse_lazy('admin:blog_post_changelist'),
                        'badge': 'apps.blog.callbacks.drafts_badge',
                    },
                    {
                        'title': 'Comments',
                        'icon': 'comment',
                        'link': reverse_lazy('admin:blog_comment_changelist'),
                    },
                    {
                        'title': 'Categories',
                        'icon': 'category',
                        'link': reverse_lazy('admin:blog_category_changelist'),
                    },
                    {
                        'title': 'Tags',
                        'icon': 'label',
                        'link': reverse_lazy('admin:blog_tag_changelist'),
                    },
                ],
            },
            {
                'title': 'Users & Access',
                'permission': lambda request: request.user.is_superuser,
                'items': [
                    {
                        'title': 'Users',
                        'icon': 'people',
                        'link': reverse_lazy('admin:auths_user_changelist'),
                    },
                    {
                        'title': 'Groups',
                        'icon': 'group',
                        'link': reverse_lazy('admin:auth_group_changelist'),
                    },
                ],
            },
        ],
    },
    'TABS': [
        {
            'models': [
                'blog.post',
            ],
            'items': [
                {
                    'title': 'All',
                    'link': reverse_lazy('admin:blog_post_changelist'),
                },
                {
                    'title': 'Published',
                    'link': lambda request: (
                        str(reverse_lazy('admin:blog_post_changelist')) + '?status__exact=published'
                    ),
                },
                {
                    'title': 'Drafts',
                    'link': lambda request: (
                        str(reverse_lazy('admin:blog_post_changelist')) + '?status__exact=draft'
                    ),
                },
            ],
        },
    ],
}


