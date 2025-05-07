# 🤖 Crypto Grid Bot — Панель управления

Интеллектуальный dry-run бот для анализа и моделирования сделок на фьючерсах с автоматическим Telegram-контролем.

---

## 📁 Структура проекта

```
crypto_grid_bot/
├── main.py                  # Точка входа (анализ + dry-run)
├── config.json              # Настройки бота
├── positions.json           # Открытые позиции (dry-run)
├── history.json             # Закрытые сделки
├── tp_sl_config.json        # Настройки TP/SL
├── .gitignore               # Исключения Git
├── requirements.txt         # Зависимости
└── modules/
    ├── strategy.py
    ├── dry_trader.py
    ├── market_analysis.py
    ├── trade_history.py
    ├── telegram_utils.py
    ├── telegram_commands.py
    ├── beta_analysis.py
    └── beta_ranker.py
```

---

## 🧠 Telegram-команды

| Команда        | Назначение                                      |
|----------------|-------------------------------------------------|
| `/status`      | Активные позиции                                |
| `/summary`     | История сделок, PnL                             |
| `/reset`       | Сброс всех dry-run позиций                      |
| `/set_tp 2.5`  | Обновить Take Profit                            |
| `/set_sl -3.0` | Обновить Stop Loss                              |

---

## 🧠 Бета-анализ (`modules/beta_ranker.py`)

Автоматически оценивает тренд BTC и расставляет приоритеты по альтам (β).

### 🚀 Автозапуск:
Если включено в `main.py`:
```python
from modules.beta_ranker import analyze_priorities
analyze_priorities()
```

### 🔹 Ручной запуск:
```bash
python modules/beta_ranker.py
```

---

## 🛠 Установка
```bash
pip install -r requirements.txt
```

## ▶️ Запуск

- Telegram бот:
```bash
python modules/telegram_commands.py
```

- Основной dry-run:
```bash
python main.py
```

---

## 📌 Контроль

- Период анализа: 5 мин по умолчанию
- Отчёты и сигналы приходят в Telegram
- Сделки и история логируются в JSON