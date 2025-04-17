# 📝 ToDo FastAPI App

Полноценное веб-приложение для управления задачами. Реализовано с нуля за несколько дней с авторизацией, CRUD, фильтрацией и деплоем.

## 🔧 Стек технологий

- **Python 3.11+**
- **FastAPI** + **Jinja2**
- **PostgreSQL** + **SQLAlchemy**
- **JWT** (авторизация через куки)
- **Alembic** (миграции)
- **Uvicorn**, **asyncio**
- Деплой на VPS

## ⚙ Возможности

- 🔐 Регистрация, логин, авторизация
- ✅ Создание, удаление задач
- 📆 Поддержка дедлайнов, приоритетов и фильтрации
- 🧠 Чистая архитектура с разделением на роуты, схемы, модели
- 🌐 Адаптивный UI на Bootstrap

## 💻 Запуск проекта

```bash
git clone https://github.com/johnnyOld/todo-fastapi-app.git
cd todo-fastapi-app
python -m venv .venv
source .venv/bin/activate  # для Mac/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 🔗 Демо и доступ

🖥 Демо: [http://45.10.43.71:8000/]

## 👨‍💻 О проекте

Проект написан за короткий срок изучения Python, как один из первых осознанных pet-проектов:
-	Без туториалов, с разбором документации и гуглом
-	Особое внимание уделено структуре и чистоте кода
-	Вдохновлён задачами из жизни (бот по резюме и менеджер задач)
