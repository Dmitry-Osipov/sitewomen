# Информационный сайт про известных женщин с использованием фреймворка Django 4.2.1 и Python 3.11.
## Структура папок.
sitewomen - sources root:
- notes - справочная информация по созданию такого сайта на Django 4;
- sitewomen - пакет конфигурации;
    - __init__.py - файл указывает питону, что данная директория является пакетом;
    - asgi.py - ;
    - settings.py - файл настроек сайта;
    - urls.py - файл для хранения всех перенаправлений клиента;
    - wsgi.py - .
- women - пакет основного приложения;
    - migrations - пакет служит для хранения миграций БД;
    - __init__.py - файл указывает питону, что данная директория является пакетом;
    - admin.py – файл для настройки админ-панели сайта (админ-панель поставляется совместно с Django и каждый сайт может сразу ее использовать);
    - apps.py – файл для настройки (конфигурирования) текущего приложения;
    - models.py – файл для хранения ORM-моделей для представления данных из базы данных;
    - tests.py – модуль с тестирующими процедурами;
    - urls.py - файл для хранения всех перенаправлений клиента;
    - views.py – файл для хранения представлений (контроллеров) текущего приложения. 
- db.sqlite3 - база данных сайта;
- manage.py - файл, который передаёт команды django-admin и выполняет их "от лица" сайта.