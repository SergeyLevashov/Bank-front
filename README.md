# Bank-front: Multi-Banking Comparison Dashboard

Платформа для сравнения банковских продуктов с поддержкой **multi-banking** и **интерактивных графиков**.

## Новые возможности

### ✅ Multi-Banking Support
- **Выпадающие списки банков** вместо ручного ввода
- **Множественный выбор конкурентов** в Urgent Mode
- **Множественный выбор банков** в Trends Mode
- Автоматическая загрузка списка банков из `configs/bank_data/`

### 📊 Chart System
- **Plotly графики** для визуализации сравнений
- **Интерактивные графики трендов**
- Интеграция `chart_generator.py` и `chart_generator_enhanced.py`
- Отображение графиков в превью отчёта

## Архитектура

```
Bank-front/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── banks.py         # NEW: Banks API endpoint
│   │   │   ├── urgent.py        # Urgent mode endpoint
│   │   │   └── trends.py        # Trends mode endpoint
│   │   ├── schemas.py        # UPDATED: Multi-bank schemas
│   │   └── main.py           # UPDATED: Added banks router
│   ├── modules/
│   │   ├── chart_generator.py
│   │   ├── chart_generator_enhanced.py
│   │   └── multi_bank_comparator.py
│   └── configs/
│       └── bank_data/        # Bank configuration files
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── UrgentForm.jsx    # UPDATED: Multi-select dropdowns
    │   │   ├── TrendsForm.jsx    # UPDATED: Multi-select dropdowns
    │   │   └── OutputPreview.jsx # UPDATED: Chart display
    │   └── lib/
    │       └── api.js            # UPDATED: Added fetchAvailableBanks
    └── package.json
```

## Установка

### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Запуск

### Backend (Terminal 1)

```bash
cd backend
python run.py
```

Backend запустится на `http://localhost:9000`

### Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend запустится на `http://localhost:5173`

## API Endpoints

### 🏛️ GET `/api/banks/available`
Возвращает список доступных банков:

```json
{
  "all": ["Альфа-Банк", "ВТБ", "Сбербанк", ...],
  "by_product": {
    "debit": ["Сбербанк", "ВТБ", ...],
    "credit": ["Альфа-Банк", ...]
  },
  "product_types": ["Кредитная карта", ...]
}
```

### 📥 POST `/api/urgent/`

Urgent mode с multi-banking:

**Request:**
```json
{
  "bank_name": "Сбербанк",
  "competitor_names": ["ВТБ", "Альфа-Банк", "Т-Банк"],
  "product_type": "Кредитная карта"
}
```

**Response:**
```json
{
  "bank_name": "Сбербанк",
  "competitor_names": ["ВТБ", "Альфа-Банк"],
  "product_type": "Кредитная карта",
  "generated_at": "2025-11-23T...",
  "comparison_table": [...],
  "insights": [...],
  "charts": {
    "comparison_chart": "<div>...Plotly HTML...</div>"
  }
}
```

### 📈 POST `/api/trends/`

Trends mode с multi-banking:

**Request:**
```json
{
  "bank_names": ["Сбербанк", "ВТБ", "Альфа-Банк"],
  "product_type": "Кредитная карта",
  "period": "12m"
}
```

**Response:**
```json
{
  "bank_names": ["Сбербанк", "ВТБ"],
  "product_type": "Кредитная карта",
  "period": "12m",
  "generated_at": "2025-11-23T...",
  "summary": [...],
  "points": [...],
  "charts": {
    "trends_chart": "<div>...Plotly HTML...</div>",
    "comparison_chart": "<div>...Plotly HTML...</div>"
  }
}
```

## Использование

### Urgent Mode (Быстрое сравнение)

1. Выберите **базовый банк** (например, Сбербанк)
2. Отметьте **несколько конкурентов** (ВТБ, Альфа-Банк, Т-Банк...)
3. Выберите **тип продукта**
4. Нажмите **"Сгенерировать отчёт"**

Результат:
- Сравнительная таблица параметров
- Ключевые инсайты
- Интерактивные графики сравнения

### Trends Mode (Анализ трендов)

1. Отметьте **несколько банков** для сравнения трендов
2. Укажите **тип продукта**
3. Выберите **период** (6 или 12 месяцев)
4. Нажмите **"Построить тренды"**

Результат:
- Динамика изменения параметров
- Резюме по трендам
- Интерактивные графики трендов

## Добавление новых банков

Добавьте JSON файл в `backend/configs/bank_data/`:

```json
{
  "bank": "Новый Банк",
  "product_type": "debit_card",
  "annual_fee": "0",
  "cashback": "1%",
  "interest_rate": "5%"
}
```

Банк автоматически появится в выпадающих списках!

## Технологии

### Backend
- **FastAPI** - современный async web framework
- **Plotly** - интерактивные графики
- **Pydantic** - валидация данных

### Frontend
- **React 18** + **Vite**
- **TailwindCSS** - стилизация
- **Native Fetch API** - HTTP запросы

## Траблшутинг

### Порт 9000 занят

```bash
# Windows
netstat -ano | findstr :9000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :9000
kill -9 <PID>
```

### Frontend не подключается к Backend

Проверьте `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:9000
```

## Лицензия

MIT License

## Автор

SergeyLevashov
