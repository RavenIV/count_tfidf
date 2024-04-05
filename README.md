# TF-IDF Counter

Веб-приложение для расчета метрики [TF-IDF](https://ru.wikipedia.org/wiki/TF-IDF).

TF и IDF рассчитываются только для текстовых файлов в формате .txt.

Морфологические особенности не учитываются (например, "яблоко" и "яблоки" будут обработаны как два разных слова).

При расчете IDF в качестве корпуса документов учитываются только ранее обработанные приложением файлы. Поэтому при запуске приложения с ненаполненной БД IDF для первого загруженного документа будет рассчитан как log(1).

После обработки файла на странице отображаются метрики для 50 слов документа, осортированных в порядке уменьшения IDF.

## Cтек

- Python 3.9
- Django 4.2
- django-bootstrap5
- SQLite

## Запустить проект локально

Клонировать репозиторий и перейти в него в командной строке:

```
git clone <repository link>
```
```
cd count_tfidf
```
Создать и активировать виртуальное окружение:

```
python3 -m venv env
```

- Для пользователей Linux/macOS

```
source env/bin/activate
```

- Для пользователей windows

```
source env/scripts/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перейти в директорию /tf_idf и выполнить миграции:

```
cd tf_idf
python manage.py migrate
```

Запустить приложение:
```
python manage.py runserver
```

## Запустить проект в docker

В директории infra/ заготовлен docker-compose для запуска проекта в контейнерах docker.

```
cd infra
```

Для использования PostgreSQL нужно заполнить .env по .env.example. Если не указать ```USE_POSTGRES```, будет использоваться SQLite.

Для запуска проекта в режиме дебаггинга в .env указать: ```DEBUG=True```

Выполнить команду:

```
docker compose up -d
```

Применить миграции:

```
docker compose exec django python manage.py migrate
```

Проект будет доступен на http://localhost:8000


## Разработчики

* [Irina Vorontsova](https://github.com/RavenIV)
