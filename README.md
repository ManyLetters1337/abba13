
# Развёртывание проекта на сервере

## 1. Установить необходимые пакеты

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git nginx postgresql postgresql-contrib
```

## 2. Клонировать Github репозиторий

```bash
git clone https://github.com/ManyLetters1337/abba13.git
cd abba13
```

## 3. Создать виртуальное окружение и установить необходимые python библиотеки 

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Создать базу данных в Postgres, создать пользователя базы данных и дать ему права

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE test_json;
CREATE USER json_user WITH PASSWORD 'YOUR_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE test_json TO json_user;
```

Обновить настройки в `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_json',
        'USER': 'json_user',
        'PASSWORD': 'YOUR_PASSWORD',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

## 5. Применить миграции к Базе данных

```bash
python manage.py migrate
```

## 6. Настроить systemd-сервис для запуска Gunicorn

Создать файл:  
`/etc/systemd/system/gunicorn.service`

```ini
[Unit]
Description=gunicorn daemon for Django app
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/youruser/abba13
ExecStart=/home/youruser/abba13/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/youruser/abba13/gunicorn.sock project.wsgi:application

[Install]
WantedBy=multi-user.target
```

Перезапустить конфигурацию systemd и запустить сервис и активировать автозапуск сервера

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload

sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## 7. Создать файл настроек nginx 

Создай файл:  
`/etc/nginx/sites-available/abba13`

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /home/youruser/abba13;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/youruser/abba13/gunicorn.sock;
    }
}
```

Активировать файл настроек через создание ссылки:

```bash
sudo ln -s /etc/nginx/sites-available/abba13 /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```
