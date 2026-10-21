# Deadlock Stater Bot

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white) ![discord.py](https://img.shields.io/badge/discord.py-2.x-5865F2?logo=discord&logoColor=white) ![Status](https://img.shields.io/badge/status-in%20development-yellow)
> **Бот находится в стадии активной разработки.**
> Команды, их названия и поведение могут меняться без предупреждения.
> Если вы нашли баг или у вас есть идея - создайте [issue](https://github.com/Sta4ik/deadlock-discord-stats/issues).

> Discord-бот для статистики Deadlock: матчи, герои, лидерборды, патчи, прицелы и т.д. - всё в одном месте.

---
## О боте
**Deadlock Stater Bot** - Discord-бот, который берёт данные из [Deadlock API](https://api.deadlock-api.com) и превращает их в удобные эмбеды прямо на вашем сервере.

Больше не нужно открывать сторонние сайты: узнать последний матч, посмотреть винрейт героя или проверить, вышел ли новый патч - теперь всё это можно посмотреть прямо в дискорд через команды с префиксом `#`.

---

## Возможности

### Общие

| Команда | Алиасы | Описание |
|---------|--------|----------|
| `#ping` | - | Проверка работоспособности бота |
| `#helpс` | - | Список всех команд |

### Игроки

| Команда | Алиасы | Описание |
|---------|--------|----------|
| `#last [deadlock_id]` | `#last_match` | Последний матч игрока: герой, K/D/A, нетворс, длительность, результат |
| `#getid [steam_id]` | - | Получить Deadlock ID по SteamID64 |
| `#whois [account_id]` | - | Steam-профиль по Deadlock ID: имя, аватар, матчи за 30 дней, ранг |

### Лидерборд

| Команда | Алиасы | Описание |
|---------|--------|----------|
| `#lead [регион]` | `#leaderbord` | Топ-10 игроков в регионе |

Доступные регионы: `Europe` · `Asia` · `NAmerica` · `SAmerica` · `Oceania`

### Герои

| Команда | Алиасы | Описание |
|---------|--------|----------|
| `#herostats` | - | Статистика всех героев: винрейт, K/D/A, урон, нетворс (за 30 дней) |

### Патчи

| Команда | Алиасы | Описание |
|---------|--------|----------|
| `#patch` | `#patch_info` | Последний патч Deadlock: заголовок, источник, дата |

### Прицелы

| Команда | Алиасы | Описание |
|---------|--------|----------|
| `#crosshair [код]` | - | Изображение прицела по коду |

---

## Установка

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Sta4ik/deadlock-discord-stats.git
cd deadlock-discord-stats
```

### 2. Создайте виртуальное окружение

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Настройте `.env`

Создайте файл `.env` в корне проекта:

```env
TOKEN=Ваш токен от дискорд бота
```

> Токен бота берётся в [Discord Developer Portal](https://discord.com/developers/applications) → ваше приложение → **Bot** → **Token**.

### 5. Запустите бота

```bash
python main.py
```

---

## Настройка Discord

1. Перейдите в [Discord Developer Portal](https://discord.com/developers/applications).
2. Создайте приложение → вкладка **Bot** → **Reset Token** и скопируйте токен.
3. В разделе **Privileged Gateway Intents** включите:
   - **Message Content Intent** - без него бот не увидит команды.
4. Вкладка **OAuth2 → URL Generator**:
   - Scopes: `bot`
   - Bot Permissions: `Send Messages`, `Embed Links`, `Attach Files`
5. Откройте сгенерированную ссылку и пригласите бота на сервер.

---

## Известные ограничения

- **Rate limit Discord**: команда `#herostats` отправляет по одному эмбеду на героя с паузой `0.5s`, чтобы не попасть под лимит. Для 20+ героев это ~10 секунд.

---

## Contributing

PR и issue приветствуются! Если нашли баг или хотите добавить команду - создайте issue с описанием.

1. Fork → `git checkout -b feature/my-feature`
2. Commit → `git commit -m "Add my feature"`
3. Push → `git push origin feature/my-feature`
4. Откройте Pull Request

---

##  Благодарности

- [Deadlock API](https://api.deadlock-api.com) - за бесплатный публичный API
- [discord.py](https://github.com/Rapptz/discord.py) - за удобную библиотеку
- Сообществу Deadlock - за игру, ради которой всё это

---

<p align="center">
  Сделано с ❤️ для сообщества Deadlock
</p>