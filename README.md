# Информационный сайт про известных женщин с использованием фреймворка Django 4.2.1 и Python 3.11.
## Структура папок.
sitewomen - sources root:
- notes - справочная пошаговая информация по созданию такого сайта на Django 4;
- sitewomen - пакет конфигурации:
    - __init__.py - файл указывает питону, что данная директория является пакетом;
    - asgi.py - ;
    - settings.py - файл настроек сайта;
    - urls.py - файл для хранения всех перенаправлений клиента;
    - wsgi.py - .
- templates - папка с HTML-шаблонами:
    - base.html - базовый шаблон для всех страниц сайта.
- women - пакет основного приложения:
    - migrations - пакет служит для хранения миграций БД;
    - templates - директория с шаблонами текущего приложения:
        - women - директория служит для избежания коллизий с другими приложениями: 
            - includes - папка для устранения дублирования кода в HTML-файлах:
                - nav.html - файл для удаления дублирования блока nav для отображения категорий. 
            - about.html - страница "О сайте"; 
            - index.html - главная страница сайта;
            - main_filters.html - страница наглядной демонстрации возможностей стандартных фильтров шаблонизатора Django.
    - __init__.py - файл указывает питону, что данная директория является пакетом;
    - admin.py – файл для настройки админ-панели сайта (админ-панель поставляется совместно с Django и каждый сайт может сразу ее использовать);
    - apps.py – файл для настройки (конфигурирования) текущего приложения;
    - converters.py - файл для пользовательских конвертеров;
    - models.py – файл для хранения ORM-моделей для представления данных из базы данных;
    - tests.py – модуль с тестирующими процедурами;
    - urls.py - файл для хранения всех перенаправлений клиента;
    - views.py – файл для хранения представлений (контроллеров) текущего приложения. 
- db.sqlite3 - база данных сайта;
- manage.py - файл, который передаёт команды django-admin и выполняет их "от лица" сайта.