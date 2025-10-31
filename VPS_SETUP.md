# Инструкция по установке и настройке VPS

## Подготовка VPS (Ubuntu/Debian)

1. Подключитесь к вашему VPS через SSH:
```bash
ssh username@your_vps_ip
```

2. Обновите систему:
```bash
sudo apt update && sudo apt upgrade -y
```

3. Установите необходимые пакеты:
```bash
sudo apt install -y curl git docker.io docker-compose
```

4. Добавьте вашего пользователя в группу docker:
```bash
sudo usermod -aG docker $USER
# Перезайдите в систему или выполните:
newgrp docker
```

## Настройка проекта

1. Создайте директорию для проекта:
```bash
sudo mkdir -p /opt/tgbot
sudo chown $USER:$USER /opt/tgbot
cd /opt/tgbot
```

2. Склонируйте репозиторий:
```bash
git clone https://github.com/your-username/your-repo.git .
```

3. Настройте переменные окружения:
```bash
# Создайте и отредактируйте .env файл
cp .env.template .env
nano .env

# Установите правильные разрешения
chmod 600 .env
```

4. Создайте директорию для логов:
```bash
mkdir -p logs
chmod 755 logs
```

## Запуск бота

### Через Docker (рекомендуется)

1. Соберите и запустите контейнер:
```bash
docker-compose up -d
```

2. Проверьте статус:
```bash
docker-compose ps
docker-compose logs -f
```

### Управление ботом

- Перезапуск бота:
```bash
docker-compose restart
```

- Остановка:
```bash
docker-compose down
```

- Обновление после изменений в коде:
```bash
git pull
docker-compose up -d --build
```

## Настройка автоматического обновления (опционально)

1. Создайте скрипт обновления:
```bash
cat > update.sh << 'EOF'
#!/bin/bash
cd /opt/tgbot
git pull
docker-compose up -d --build
EOF

chmod +x update.sh
```

2. Добавьте в crontab для проверки обновлений каждый час:
```bash
# Отредактируйте crontab
crontab -e

# Добавьте строку:
0 * * * * /opt/tgbot/update.sh >> /opt/tgbot/logs/update.log 2>&1
```

## Мониторинг и обслуживание

### Просмотр логов

```bash
# Все логи
docker-compose logs

# Последние логи с отслеживанием
docker-compose logs -f

# Последние 100 строк
docker-compose logs --tail=100
```

### Проверка статуса

```bash
# Статус контейнера
docker-compose ps

# Использование ресурсов
docker stats
```

### Очистка логов

```bash
# Если логи занимают много места
sudo truncate -s 0 /opt/tgbot/logs/*.log
```

## Безопасность

1. Настройте firewall (UFW):
```bash
sudo apt install ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
```

2. Установите fail2ban для защиты от брут-форса:
```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

3. Регулярно обновляйте систему:
```bash
# Добавьте в crontab
0 0 * * 0 apt update && apt upgrade -y
```

## Резервное копирование

1. Настройте скрипт бэкапа:
```bash
#!/bin/bash
BACKUP_DIR="/root/backups"
mkdir -p $BACKUP_DIR
cd /opt/tgbot
tar -czf $BACKUP_DIR/tgbot-$(date +%Y%m%d).tar.gz .env logs/
find $BACKUP_DIR -type f -mtime +7 -delete
```

2. Добавьте в crontab для ежедневного бэкапа:
```bash
0 0 * * * /opt/tgbot/backup.sh
```