"""
Django settings for sitewomen project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hgqe908f-+$58m@$(pi^lto%!x%^3&2@du*u9i51(_fhy(-^an'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Переменная служит для более удобной отладки сайта, для боевого сервера её следует отключить.

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'sitewomen.ru']  # Здесь требуется указывать разрешённые хосты, когда мы
# будем заселять сайт на сервер.

INTERNAL_IPS = ['127.0.0.1']  # Добавили коллекцию внутренних IP (в т.ч. для django debug toolbar).


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # Настройка нужна, чтобы Django мог подключить статические файлы к проекту.
    'django_extensions',  # Добавил стороннее одноимённое расширение для оболочки Django.
    'women.apps.WomenConfig',  # Добавляем своё приложение, чтобы Django работал с ним. Прим.: по идее достаточно просто
    # написать имя приложения (women), но в действительности Django обращаясь к пакету women, берёт файл apps.py и
    # настройки из класса WomenConfig, поэтому мы явно пропишем путь к этому классу. Прим. 2: также чтобы шаблоны
    # находились, мы прописали здесь само приложение. Если бы мы этого не сделали, то шаблоны не отработали.
    'users.apps.UsersConfig',
    'debug_toolbar',  # Настройка для работы с инструментом django debug toolbar.
    'social_django',  # Настройка OAuth 2.0.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Ещё одна настройка для работы django debug toolbar.
]

ROOT_URLCONF = 'sitewomen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Стандартный шаблонизатор Django.
        'DIRS': [ # Этот параметр позволяет описывать нестандартные пути к файлам-шаблонам.
            BASE_DIR / 'templates',  # константа BASE_DIR отвечает за путь к source root, а далее указываем конкретный
            # путь внутри sitewomen (которая src).
        ],
        'APP_DIRS': True,  # Параметр говорит о том, что внутри приложения надо искать подкаталоги стандартном каталоге templates.
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.get_women_context'  # Благодаря кастомному контекстному процессору нам доступно
                # меню сайта во всех шаблонах.
            ],
        },
    },
]

WSGI_APPLICATION = 'sitewomen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'  # Меняем язык проект на русский.

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Пока нам хватит только этой настройки, но ниже пропишу другие с подробным описанием:
STATIC_URL = 'static/'  # префикс URL-адреса для статических файлов.
# STATIC_ROOT - путь к общей статической папке, формируемой при запуске команды collectstatic (для сбора всей статики в
# единый каталог при размещении сайта на реальном веб-сервере).
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]  # список дополнительных (нестандартных путей к статическим файлам, используемых для сбора и для
# режима отладки). Пример: STATICFILES_DIRS = [ BASE_DIR / 'sitewomen/static' ] - если static в пакете конфигурации.
# Примечание: при DEBUG = False статика не ищется автоматически в подкаталогах static приложения women

# Все эти константы нужны потому, что существует следующая иерархия статических папок:
# sitewomen
#     |
#     |---sitewomen
#     |       |
#     |       \---static - нестандартный путь
#     |
#     |---women
#     |     |
#     |     |---static - стандартный путь
#     |     |
#     |     \---templates
#     |
#     \---static - общая папка проекта (сюда потребуется перенести всю статику командой collectstatic при деплое)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

MEDIA_ROOT = BASE_DIR / 'media'  # Указываем папку, в которую будут загружаться все переданные файлы.
MEDIA_URL = '/media/'  # Добавляем префикс media ко всем файлам.

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Определяем константы, которые отвечают за перенаправления:
LOGIN_REDIRECT_URL = 'home'  # задаёт URL-адрес, на который следует перенаправлять пользователя после успешной авторизации.
LOGIN_URL = 'users:login'  # определяет URL-адрес, на который следует перенаправлять неавторизованного пользователя при
# попытке посетить закрытую страницу сайта.
LOGOUT_REDIRECT_URL = 'home'  # задаёт URL-адрес, на который перенаправляется пользователь после выхода.

AUTHENTICATION_BACKENDS = [  # Указываем модули бэкенда для авторизации.
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'users.authentication.EmailAuthBackend',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Модуль почтового бэкенда.

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'storm-yes@yandex.ru'
EMAIL_HOST_PASSWORD = 'zxqfkhabmgazkget'
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

AUTH_USER_MODEL = 'users.User'

DEFAULT_USER_IMAGE = MEDIA_URL + 'users/default.png'

SOCIAL_AUTH_GITHUB_KEY = '8db5a4783a8caf0f87ab'
SOCIAL_AUTH_GITHUB_SECRET = '392a0458422f640008f447bae6587282ec763fa8'

SOCIAL_AUTH_VK_OAUTH2_KEY = '51803725'
SOCIAL_AUTH_VK_OAUTH2_SECRET = '9Pbls3oEa4TN1k7kAMA7'
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']  # Дополнительно берём почту у прошедших аутентификацию через VK.

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'users.pipeline.new_users_handler',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
