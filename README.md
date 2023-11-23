# Информационный сайт про известных женщин с использованием фреймворка Django 4.2.1 и Python 3.11.
## Структура папок.
sitewomen - sources root:
- media - директория со всеми графическими файлами клиентов:
    - photos - директория переданных изображений от пользователя со страницы "Добавить статью"; 
    - uploads_model - директория переданных изображений пользователя со страницы "О сайте". 
- notes - справочная пошаговая информация по созданию такого сайта на Django 4;
- sitewomen - пакет конфигурации:
    - __init__.py - файл указывает питону, что данная директория является пакетом;
    - asgi.py - это точка входа для веб-серверов, которые поддерживают ASGI (Asynchronous Server Gateway Interface);
    - settings.py - файл настроек сайта;
    - urls.py - файл для хранения всех перенаправлений клиента;
    - wsgi.py -  это точка входа для веб-серверов, которые поддерживают WSGI (Web Server Gateway Interface).
- static - папка оформления для админ-панели;
- templates - папка с HTML-шаблонами:
    - admin - папка с HTML-шаблонами для админ-панели:
        - base_site.html - базовый шаблон админ-панели.
    - base.html - базовый шаблон для всех страниц сайта.
- users - пакет модуля авторизации:
    - migrations - пакет служит для хранения миграций БД;
    - templates - директория с шаблонами текущего приложения:
        - users - директория служит для избежания коллизий с другими приложениями: 
            - login.html - страница входа.
    - __init__.py - файл указывает питону, что данная директория является пакетом;
    - admin.py – файл для настройки админ-панели сайта (админ-панель поставляется совместно с Django и каждый сайт может сразу ее использовать);
    - apps.py – файл для настройки (конфигурирования) текущего приложения;
    - context_processors.py - файл с шаблонным контекстным процессором;
    - forms.py - файл для классов формы;
    - models.py – файл для хранения ORM-моделей для представления данных из базы данных;
    - tests.py – модуль с тестирующими процедурами;
    - urls.py - файл для хранения всех перенаправлений клиента;
    - views.py – файл для хранения представлений (контроллеров) текущего приложения. 
- women - пакет основного приложения:
    - migrations - пакет служит для хранения миграций БД;
    - static - папка со статикой для приложения women:
        - women - директория служит для избежания коллизий с другими приложениями:  
            - css - папка для стилей оформления;
            - js - папка для javascript;
            - images - папка для изображений.
    - templates - директория с шаблонами текущего приложения:
        - women - директория служит для избежания коллизий с другими приложениями: 
            - includes - папка для устранения дублирования кода в HTML-файлах:
                - nav.html - файл для удаления дублирования блока nav для отображения категорий. 
            - about.html - страница "О сайте"; 
            - addpage.html - страница создания поста пользователем;
            - index.html - главная страница сайта;
            - list_categories.html - блок отображения категорий постов;
            - list_tags.html - блок отображения тегов постов;
            - main_filters.html - страница наглядной демонстрации возможностей стандартных фильтров шаблонизатора Django;
            - post.html - страница отображения конкретного поста.
    - templatetags - пакет для создания пользовательских тегов:
        - __init__.py - файл указывает питону, что данная директория является пакетом;
        - women_tags - файл содержит пользовательские теги.
    - __init__.py - файл указывает питону, что данная директория является пакетом;
    - admin.py – файл для настройки админ-панели сайта (админ-панель поставляется совместно с Django и каждый сайт может сразу ее использовать);
    - apps.py – файл для настройки (конфигурирования) текущего приложения;
    - converters.py - файл для пользовательских конвертеров;
    - forms.py - файл для классов формы;
    - models.py – файл для хранения ORM-моделей для представления данных из базы данных;
    - tests.py – модуль с тестирующими процедурами;
    - urls.py - файл для хранения всех перенаправлений клиента;
    - utils.py - файл со всеми дополнительными вспомогательными классами;
    - views.py – файл для хранения представлений (контроллеров) текущего приложения. 
- db.sqlite3 - база данных сайта;
- manage.py - файл, который передаёт команды django-admin и выполняет их "от лица" сайта.