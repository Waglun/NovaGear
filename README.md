# NovaGear

Интернет-магазин по модели дропшипинга, разработанный на Django.

## Технологии

- Python 3.12
- Django 5
- PostgreSQL
- HTMX
- Alpine.js
- Bootstrap / Tailwind CSS
- Celery
- Redis
- Gunicorn
- Nginx

## Функционал

### Пользователи
- Регистрация
- Авторизация
- Восстановление пароля
- Профиль пользователя

### Каталог
- Категории товаров
- Поиск
- Фильтрация
- Карточка товара

### Покупки
- Корзина
- Оформление заказа
- История заказов

### Администрирование
- Управление товарами
- Управление заказами
- Управление пользователями

## Установка

### Клонирование проекта

```bash
git clone <repository_url>
cd config
```

### Создание виртуального окружения

```bash
python -m venv djvenv
```

### Активация

Windows:

```bash
djvenv\Scripts\activate
```

Linux/macOS:

```bash
source djvenv/bin/activate
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`.

### Выполнение миграций

```bash
python manage.py migrate
```

### Создание суперпользователя

```bash
python manage.py createsuperuser
```

### Запуск сервера

```bash
python manage.py runserver
```

Сайт будет доступен по адресу:

```text
http://127.0.0.1:8000/
```

## Структура проекта

```text
NovaGear/
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── manage.py
├── config/
├── apps/
├── static/
├── media/
└── templates/
```

## Статус проекта

🚧 Проект находится в активной разработке.