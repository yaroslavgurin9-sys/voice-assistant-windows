# Настройка Voice Assistant for Windows

## Предварительные требования

### Системные
- **Windows 10** или **Windows 11**
- **Python 3.8+** ([скачать](https://www.python.org/downloads/))
- **~2 ГБ** вольного места на диске
- **Микрофон** (интегрированный или USB)

### Программы
- **Git** ([скачать](https://git-scm.com/download/win))
- **Visual C++ Build Tools** (для pyaudio)
  - Нижняя граница: [https://visualstudio.microsoft.com/downloads/](https://visualstudio.microsoft.com/downloads/)

## Пошаговая инсталляция

### 1. Клонируем репозиторий

```bash
git clone https://github.com/yaroslavgurin9-sys/voice-assistant-windows.git
cd voice-assistant-windows
```

### 2. Создаем виртуальное окружение

```bash
# Открываем CMD или PowerShell в директории проекта

python -m venv venv

# Активируем
.\venv\Scripts\activate
```

После активации вы должны видеть `(venv)` в промпте.

### 3. Устанавливаем зависимости

```bash
# Обновляем pip
python -m pip install --upgrade pip

# Устанавливаем базовые зависимости
pip install -r requirements.txt
```

**Примечание:** Если у вас проблемы с установкой pyaudio:

```bash
# вариант 1: используем pipwin
pip install pipwin
pipwin install pyaudio

# вариант 2: скачиваем выстроенные колеса с https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
где ваша версия Python 3.8+ и Windows x64
```

### 4. Скачиваем модель Vosk

**От руки (рекомендуется):**

1. Откройте [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)
2. Скачайте русскую модель: **vosk-model-ru-0.42-big** (~150 MB)
3. Распакуйте в новый фолдер: `models/vosk_models/vosk-model-ru-0.42-big/`

Проверьте структуру:
```
models/vosk_models/
└── vosk-model-ru-0.42-big/
    ├── am/
    ├── conf/
    └── graph/
```

**Командная строка (по желанию):**

```bash
mkdir -p models/vosk_models
cd models/vosk_models
# Скачайте и распакуйте выше упомянутые данные
cd ../..
```

### 5. Настраиваем окружение

```bash
# Копируем конфиг
# Главное имени: Меню Windows -> Найти -> "cmd" -> ОК
# Пастюем две команды:

copy .env.example .env

# Отредактируйте .env файл (опционально)
notebook .env

# или откройте в Коде VSCode .env
code .env
```

### 6. Проверяям микрофон

Чтобы получить информацию о микрофонах:

```bash
python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\'name\']}') for i in range(p.get_device_count())]"
```

Вам понадобится это для онаинка `AUDIO_DEVICE_INDEX` в `.env` если требуется.

### 7. Делаем пробные запуски

**Проверяям конфигурацию:**

```bash
python -c "from config.settings import config; print('Configuration loaded successfully')"
```

**Открываем ассистент (консольный режим):**

```bash
python main.py
```

После вывода "Он готов!" - испытайте команды.

## Открытие ассистента

### Вариант 1: Консольный режим

```bash
python main.py
```

### Вариант 2: GUI режим

1. Отредактируйте `.env` и установите:
   ```
   GUI_USE_GUI=True
   ```

2. Например, зарегистрируютесь в оци и руните:
   ```bash
   python main.py
   ```

### Вариант 3: Быстрый запуск Windows

```bash
run.bat
```

## Решение дроблем

### Проблема: Vosk модель не найдена

**Ошибка:**
```
FileNotFoundError: Model not found at ./models/vosk_models/vosk-model-ru-0.42-big
```

**Решение:**
1. Проверьте путь в .env
2. Отгружайте полную модель от https://alphacephei.com/vosk/models

### Проблема: pyaudio не устанавливается

**Ошибка:**
```
error: Microsoft Visual C++ 14.0 or greater is required
```

**решение:**
1. Осылание на Visual C++ Build Tools: https://visualstudio.microsoft.com/downloads/
2. Уверены, что выбраны десктоп разработки C++
3. Попробуйте pipwin:
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

### Проблема: "Не распознана речь"

1. Управление томом аудио на Windows
2. Проверьте микрофон приятость до 16 КГц
3. Проверьте VAD параметры в .env

## Опционально: Создание шорткута На КОМПьЮТЕРЕ

1. Откройте Проводник
2. Перейти в директорию проекта
3. Кликните по рун.bat правой кнопкой
4. "Отправить" -> "На десктоп (новый шорткут)"

## Удачные проверки

На этапе вы видите:
- ✅ "Откнюта ъндия веы готов" - окстредование всех модулей
- ✅ "Ассистент готов!" - готов к приютию зда вездеспособности
- ✅ "Ассистент выключен" (не НОНОН) Эца вывстить

## ЭТУП НАСТОЙКи

Подключение читайте README.md для деталей.
