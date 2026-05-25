# JobBureau

> Онлайн-платформа бюро по трудоустройству — соединяем соискателей и работодателей.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=flat-square&logo=django&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-11-003545?style=flat-square&logo=mariadb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-alpine-009639?style=flat-square&logo=nginx&logoColor=white)

---

## Возможности

### Для соискателей
- Регистрация и личный кабинет
- Несколько резюме на одном аккаунте (PDF + текстовая информация)
- Хранение паспорта и трудовой книжки (сканы)
- Отклики на вакансии с сопроводительным письмом
- Отслеживание статусов откликов

### Для работодателей
- Профиль компании с логотипом и верификацией
- Публикация вакансий с гибкими настройками
- Просмотр откликов с резюме соискателей
- Аналитика по вакансиям и соискателям
- Система оплаты за принятых сотрудников

### Для администраторов
- Дашборд со статистикой в реальном времени
- Графики регистраций, откликов и доходов
- Управление пользователями и верификация работодателей

### Дизайн
- Тёмная и светлая тема с сохранением выбора
- Адаптивный интерфейс (мобильный, планшет, десктоп)
- Минималистичный editorial стиль

---

## Стек

| Слой | Технология |
|---|---|
| Backend | Django 5.0, Python 3.12 |
| База данных | MariaDB 11 |
| Web-сервер | Gunicorn + Nginx |
| Контейнеризация | Docker, Docker Compose |
| Frontend | Vanilla CSS/JS, Phosphor Icons, Chart.js |
| SSL | Let's Encrypt (Certbot) |

---

## Быстрый старт (локально)

### Требования
- Python 3.12+
- MariaDB / MySQL
- pip

```bash
# 1. Клонируй репозиторий
git clone https://github.com/username/job_bureau.git
cd job_bureau

# 2. Создай виртуальное окружение
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Установи зависимости
pip install -r requirements.txt

# 4. Создай .env
cp .env.example .env
# Открой .env и заполни переменные

# 5. Создай базу данных
mysql -u root -p -e "CREATE DATABASE job_bureau CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 6. Миграции
python manage.py makemigrations accounts applicants employers vacancies payments
python manage.py migrate

# 7. Суперпользователь (для доступа к /dashboard/)
python manage.py createsuperuser

# 8. Запуск
python manage.py runserver
```

Открывай → http://127.0.0.1:8000

---

## Деплой на сервер (Docker)

### Требования на сервере
- Ubuntu 22.04+
- Docker Engine
- Docker Compose v2

### Установка Docker (если нет)
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Перелогинься
```

### Развёртывание

```bash
# 1. Клонируй репозиторий
git clone https://github.com/username/job_bureau.git
cd job_bureau

# 2. Создай .env
cp .env.example .env
nano .env
```

Заполни `.env`:
```env
SECRET_KEY=длинная-случайная-строка-минимум-50-символов
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=job_bureau
DB_USER=jobbureau
DB_PASSWORD=надёжный-пароль-бд
DB_ROOT_PASSWORD=надёжный-root-пароль
DB_HOST=db
DB_PORT=3306
```

```bash
# 3. Укажи домен в nginx конфиге
nano nginx/nginx.conf
# Замени yourdomain.com на свой домен

# 4. Запускай
docker compose up -d

# 5. Создай суперпользователя
docker compose exec web python manage.py createsuperuser
```

**Готово!** Сайт доступен на http://yourdomain.com

---

## SSL-сертификат (Let's Encrypt)

```bash
# Получи сертификат (домен должен уже указывать на сервер)
docker compose exec certbot certbot certonly \
  --webroot -w /var/www/certbot \
  -d yourdomain.com -d www.yourdomain.com \
  --email your@email.com --agree-tos

# Раскомментируй HTTPS блок в nginx/nginx.conf
nano nginx/nginx.conf

# Перезапусти nginx
docker compose restart nginx
```

Сертификат обновляется автоматически каждые 12 часов.

---

## Полезные команды

```bash
# Просмотр логов
docker compose logs -f web
docker compose logs -f nginx

# Перезапуск после изменений
docker compose up -d --build

# Остановка
docker compose down

# Бэкап базы данных
docker compose exec db mariadb-dump \
  -u root -p${DB_ROOT_PASSWORD} job_bureau > backup_$(date +%Y%m%d).sql

# Восстановление из бэкапа
docker compose exec -T db mariadb \
  -u root -p${DB_ROOT_PASSWORD} job_bureau < backup.sql

# Открыть shell Django
docker compose exec web python manage.py shell

# Применить миграции вручную
docker compose exec web python manage.py migrate
```

---

## Структура проекта

```
job_bureau/
├── apps/
│   ├── accounts/       # Авторизация, пользователи
│   ├── applicants/     # Соискатели, резюме, документы
│   ├── employers/      # Работодатели, аналитика
│   ├── vacancies/      # Вакансии, отклики
│   ├── payments/       # Платежи
│   └── dashboard/      # Админ-дашборд со статистикой
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   └── urls.py
├── templates/          # Глобальные шаблоны
├── static/             # CSS, JS
├── nginx/              # Конфиг Nginx
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
└── requirements.txt
```

---

## Монетизация

Платформа зарабатывает комиссию с работодателей за каждого принятого сотрудника:

```
Комиссия = (ЗП_min + ЗП_max) / 2 × 0.1%
```

Работодатель видит стоимость при создании вакансии и оплачивает все принятые отклики одним платежом из личного кабинета.

---

## Лицензия

MIT — используй свободно.
