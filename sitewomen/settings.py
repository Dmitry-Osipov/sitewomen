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

ALLOWED_HOSTS = ['127.0.0.1']  # Здесь требуется указывать разрешённые хосты, когда мы будем заселять сайт на сервер.

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
    'debug_toolbar',  # Настройка для работы с инструментом django debug toolbar.
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
# STATICFILES_DIRS - список дополнительных (нестандартных путей к статическим файлам, используемых для сбора и для
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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
