# Telegram Bot с Gemini AI

Telegram бот, использующий Gemini AI для обработки сообщений. Поддерживает развертывание через Docker для простого деплоя на VPS.

## Быстрый старт

### Локальный запуск (Windows PowerShell)

1. Создайте и активируйте виртуальное окружение:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Установите зависимости:
```powershell
pip install -r requirements.txt
```

3. Настройте переменные окружения:
```powershell
copy .env.template .env
# Отредактируйте .env и добавьте ваши токены:
# - TELEGRAM_BOT_TOKEN
# - MISTRAL_API_KEY
```

4. Запустите бота:
```powershell
python tg-bot_ai_gemimi.py
```

### Запуск через Docker (рекомендуется)

1. Установите [Docker Desktop для Windows](https://www.docker.com/products/docker-desktop/)

2. Настройте `.env` (как описано выше)

3. Запустите контейнер:
```powershell
docker compose up -d
```

4. Просмотр логов:
```powershell
docker compose logs -f
```

## Деплой на VPS

Подробная инструкция по установке на VPS находится в файле [VPS_SETUP.md](VPS_SETUP.md).

Краткая версия для Docker:
```bash
# На VPS
mkdir -p /opt/tgbot && cd /opt/tgbot
git clone <your-repo-url> .
cp .env.template .env
nano .env  # добавьте токены
docker-compose up -d
```

## Переменные окружения

Создайте файл `.env` на основе `.env.template`:

```env
# Токены
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
MISTRAL_API_KEY=your_mistral_api_key_here

# Настройки Mistral AI
MISTRAL_MODEL=mistral-small-latest

# Логирование (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
```

## Управление ботом

### Docker команды

```bash
# Запуск
docker compose up -d

# Просмотр логов
docker compose logs -f

# Перезапуск
docker compose restart

# Остановка
docker compose down

# Обновление после изменений
docker compose up -d --build
```

### Мониторинг

```bash
# Статус контейнера
docker compose ps

# Использование ресурсов
docker stats
```

## Безопасность

- **Важно:** Никогда не коммитьте `.env` файл с реальными токенами
- На VPS установите права на `.env`: `chmod 600 .env`
- Используйте брандмауэр (UFW) на VPS
- Регулярно обновляйте Docker и зависимости

## Поддержка

Если возникли проблемы:
1. Проверьте логи: `docker compose logs -f`
2. Убедитесь, что все переменные в `.env` заполнены корректно
3. Проверьте подключение к интернету и доступность API Telegram/Gemini

## Разработка

Внести изменения в код:
1. Сделайте изменения в `tg-bot_ai_gemimi.py`
2. Протестируйте локально
3. Создайте коммит и запушьте в репозиторий
4. На VPS: `docker compose up -d --build`
# TG-bот с ИИ (gemini)

Небольшой Telegram-бот, использующий `aiogram` и Google Generative AI (модель Gemini).

Важно

- Не храните реальные ключи в репозитории. Если ключи попали в публичный репозиторий — немедленно отозовите их и создайте новые.

Подготовка и установка зависимостей

1) Скопируйте пример `.env` и заполните свои значения:

```powershell
cp .env.example .env
# затем откройте .env и впишите свои ключи
```

2) Установите зависимости:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Запуск бота

Вариант 1 — через переменные окружения в текущей сессии PowerShell:

```powershell
$env:GENAI_API_KEY = "ВАШ_GENAI_API_KEY"
$env:TG_BOT_TOKEN = "123456:ABCdefGhIjklmnop"
python "c:\Users\user\Documents\_VSCode_Python\3. ТГ-бот с ИИ\tg-bot ai gemimi.py"
```

Вариант 2 — поместить ключи в файл `.env` рядом со скриптом (файл загружается автоматически через `python-dotenv`):

```text
GENAI_API_KEY=ваш_ключ
TG_BOT_TOKEN=123456:ABCdefGhIjklmnop
LOG_LEVEL=INFO
LOG_FILE=bot.log
```

Если при запуске вы видите ошибку вида "GENAI_API_KEY не задана в окружении", значит переменная не установлена — проверьте `.env` или задайте переменные в сессии PowerShell как показано выше.

Тестирование

В проекте есть простой тест `tests/test_handler.py` и runner `run_tests.py`.

Запуск тестов без pytest (быстро):

```powershell
python run_tests.py
```

Запуск через pytest (если установлен):

```powershell
python -m pytest -q
```

Логирование

- По умолчанию лог записывается в `bot.log` (параметр `LOG_FILE`) и также выводится в консоль.
- Уровень логов можно настроить через `LOG_LEVEL` в `.env` (например, DEBUG, INFO).

Если нужно, могу добавить пример workflow для CI (GitHub Actions) чтобы тесты запускались автоматически и чтобы проверять, что секреты не попадают в коммиты.
