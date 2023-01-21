# FLASK 1
Домашняя работа по курсу Flask1

Для установки пакетов активируйте виртуальное окружение командой:
```
source flask_venv/bin/activate
```
и выполните команду:
```
pip install -r requirements.txt
```
Для запуска тестового веб-сервера для app-приложения выполните соответствующую команду:
```
python app.py
python app_dict.py
python app_db.py
python app_orm.py
```
Адрес доступа к API для app.py (база данных quotes.db):
```
127.0.0.1:5000
/authors            (GET, POST)
/authors/1          (GET, PUT, DELETE)
/authors/1/quotes   (POST)
/quotes             (GET)
/quotes/1           (GET, PUT, DELETE)
/quotes/filter      (GET)
```
Пример фильтрации:
```
/quotes/filter?rating=4&author_id=1
```
API-запросы для thunder (postmen) можно импортировать из файла:
```
out_json/thunder-collection_QuotesAPI(Flask1).json
```