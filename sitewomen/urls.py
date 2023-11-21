"""
URL configuration for sitewomen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the includes() function: from django.urls import includes, path
    2. Add a URL to urlpatterns:  path('blog/', includes('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from sitewomen import settings

from women import views

# Важно заметить, что как только мы добавим хотя бы 1 маршрут, то тестовая стандартная страница Django станет недоступна.
urlpatterns = [
    path('admin/', admin.site.urls),  # Первый параметр определяет суффикс URL-адреса, второй - ссылка на функцию
    # представления, которая будет автоматически вызываться при соответствующем запросе.
    path('', include('women.urls')),  # С помощью функции includes подключаем все маршруты, что были прописаны в пакете
    # приложения в файле urls.py. Если передать суффикс, то он будет добавлен ко всем маршрутам, что мы подключаем.
    path('users/', include('users.urls', namespace='users')),  # namespace - пространство имён для маршрутов users.
    # Таким образом, чтобы обратиться к функции приложения нужно прописать - <пространство имён>/<имя пути>.
    path('__debug__/', include('debug_toolbar.urls')),  # Подключаем url для django debug toolbar.
]

if settings.DEBUG:  # Связываем URL с маршрутом в режиме отладки (в боевом режиме сервер и так будет иметь необходимые
    # настройки).
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found   # Переменной-перехватчику присваиваем ссылку на функцию представления при 404 ошибке.
# Прим.: все перехватчики исключений работают только при выключенном DEBUG.

admin.site.site_header = 'Панель администрирования'  # Меняем текст хэдера админ-панели.
admin.site.index_title = 'Известные женщины мира'  # Меняем текст подзаголовка панели (тег h1).
