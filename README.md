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
            - includes - папка для устранения дублирования кода в HTML-файлах:
                - for_cycle_form.html - файл удаления дублирования цикла for шаблонов формы (без двоеточия и csrf-токена);
                - password_reset_cycle.html - файл удаления дублирования цикла for шаблонов формы (с двоеточием и csrf-токеном);
            - login.html - страница входа;
            - password_change_done.html - страница подтверждения успешного изменения пароля;
            - password_change_form.html - страница изменения пароля;
            - password_reset_complete.html - страница успешной смены пароля;
            - password_reset_confirm.html - страница подтверждения смены пароля;
            - password_reset_done.html - страница дальнейших инструкций по смене пароля;
            - password_reset_email.html - одноразовая страница указания почты;
            - password_reset_form.html - страница сброса пароля по почте;
            - profile.html - страница профиля пользователя;
            - register.html - страница регистрации нового пользователя;
            - register_done - страница продолжения после регистрации нового пользователя.
    - __init__.py - файл указывает питону, что данная директория является пакетом;
    - admin.py – файл для настройки админ-панели сайта (админ-панель поставляется совместно с Django и каждый сайт может сразу ее использовать);
    - apps.py – файл для настройки (конфигурирования) текущего приложения;
    - authentication.py - файл с модулями бекэнда для авторизации;
    - context_processors.py - файл с шаблонным контекстным процессором;
    - forms.py - файл для классов формы;
    - models.py – файл для хранения ORM-моделей для представления данных из базы данных;
    - pipeline.py - файл служит для автоматического добавления всем пользователям группы входа через соц. сети;
    - tests.py – модуль с тестирующими процедурами;
    - urls.py - файл для хранения всех перенаправлений клиента;
    - views.py – файл для хранения представлений (контроллеров) текущего приложения. 
- women - пакет основного приложения:
    - fixtures - папка служит для хранения json-объектов:
        -db.json - сгруженные данные из БД по всем таблицам, кроме social_django; 
        - women_women.json - сгруженные данные из БД по таблице Women.
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
            - contact.html - страница обратной связи;
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
    - sitemaps.py - файл для хранения записей для карты сайта;
    - tests.py – модуль с тестирующими процедурами;
    - urls.py - файл для хранения всех перенаправлений клиента;
    - utils.py - файл со всеми дополнительными вспомогательными классами;
    - views.py – файл для хранения представлений (контроллеров) текущего приложения. 
- db.sqlite3 - база данных сайта;
- manage.py - файл, который передаёт команды django-admin и выполняет их "от лица" сайта.