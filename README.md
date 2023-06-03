# Blogit

### Проект выполнен для Selectel:

[Первая часть туториала - разработка.](https://selectel.ru/blog/tutorials/django-blog/)

[Вторая часть - деплой на Gunicorn/Nginx.](https://selectel.ru/blog/tutorials/django-blog-2/)

Оригинальная версия Blogit с контактной формой для отправки сообщений через SMTP Yandex - [здесь.](https://github.com/natkaida/blogit_with_contact_form)

**Blogit** - многофункциональная соцплатформа на фреймворке Django. Включает в себя приложения:
- **users** - создание, редактирование, удаление пользовательских профилей. Аутентификация, авторизация. Добавление в друзья (и удаление из друзей). Мессенджер.
- **blog** - создание, редактирование, удаление записей. Добавление в "Избранное" и "Закладки". Вывод записей по тегам и по категориям. Комментарии, френдлента.
- **polls** - проведение опросов и голосований. Визуализация результатов с Chart.js.
- **quizzes** - проведение тестов. Вопросы с одним и с несколькими верными вариантами ответа.

Установка:
- Создайте виртуальное окружение ```python -m venv blogit\venv``` и перейдите в директорию blogit ```cd blogit```.
- Активируйте окружение ```venv\scripts\activate```.
- Установите зависимости ```pip install -r requirements.txt```
- Создайте базу данных и аккаунт администратора:
```
manage.py migrate
manage.py createsuperuser
```
### В случае появления ошибки ```OperationalError: no such table: users_profile```:

На Windows выполните:
```
manage.py migrate auth
manage.py migrate --run-syncdb
```
На Ubuntu:

```
python3 manage.py migrate auth
python3 manage.py migrate --run-syncdb
```