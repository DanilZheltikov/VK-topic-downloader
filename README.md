## VK Topic Downloader

Инструмент для выгрузки тем (топиков) и комментариев из раздела обсуждений сообщества ВКонтакте и формирования DOCX‑отчёта по заранее подготовленному шаблону.

### Возможности

- **Загрузка обсуждений ВК**: получает список тем (`board.getTopics`) по ID сообщества.
- **Загрузка всех комментариев**: выгружает все комментарии каждой темы с учётом пагинации (`board.getComments`).
- **Преобразование данных**: приводит дату из Unix‑timestamp к человекочитаемому формату `ДД.ММ.ГГГГ`.
- **Генерация DOCX‑отчёта**: заполняет шаблон `template.docx` данными и сохраняет результат в папку `output`.
- **Логирование**: пишет информативные логи в stdout (и при желании в файл).

### Требования

- **Python**: 3.11+ (рекомендуется актуальная версия 3.11/3.12)
- **Зависимости** (также перечислены в `requirements.txt`):
  - `vk-api>=11.9.0`
  - `python-dotenv>=1.0.0`
  - `pydantic>=2.0.0`
  - `docxtpl>=0.16.0`

### Установка

1. **Клонировать репозиторий**:

   ```bash
   git clone https://github.com/DanilZheltikov/VK-topic-downloader.git
   cd VK-topic-downloader
   ```

2. **Создать и активировать виртуальное окружение** (рекомендуется):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/macOS
   ```

3. **Установить зависимости**:

   ```bash
   pip install -r requirements.txt
   ```

### Настройка окружения

Проект использует `.env` для хранения секретов и настроек. Файл `.env` игнорируется Git (см. `.gitignore`), его нужно создать вручную в корне проекта.

Создайте файл `.env` и укажите:

```env
ACCESS_TOKEN=ваш_токен_доступа_VK
GROUP_ID=123456789
```

- **`ACCESS_TOKEN`**: сервисный/пользовательский токен с правами доступа к обсуждениям сообщества (board).
- **`GROUP_ID`**: числовой ID сообщества (без минуса). Например, если адрес группы `https://vk.com/public123456789`, то `GROUP_ID=123456789`.

### Запуск

После установки зависимостей и настройки `.env` выполните:

```bash
python main.py
```

Сценарий:

1. `main.py` вызывает `get_topics_with_comments` из `vk_service.py` и получает список тем с комментариями.
2. Формируется контекст для шаблона (`topics` в виде списка словарей).
3. Функция `doc_render` из `doc_formater.py` рендерит шаблон `template/template.docx` и сохраняет итоговый документ в папку `output` под именем `Topics.docx` (по умолчанию).

Готовый файл будет лежать по пути:

```text
output/Topics.docx
```

### Структура проекта

- **`main.py`**  
  Точка входа. Оркестрирует процесс:
  - получение тем и комментариев (`vk_service.get_topics_with_comments`);
  - подготовка контекста для шаблона;
  - генерация документа (`doc_formater.doc_render`);
  - логирование ошибок и завершения работы.

- **`vk_service.py`**  
  Работа с VK API:
  - `get_all_comments(vk, group_id, topic_id) -> list[Comments]` — постранично выгружает все комментарии для одной темы;
  - `get_topics_with_comments(token: str, group_id: int) -> list[Topic]` — собирает все темы и их комментарии в список объектов `Topic`.
  
  Использует:
  - `vk_api.VkApi` для авторизации по токену;
  - переменные окружения `ACCESS_TOKEN` и `GROUP_ID` (через `python-dotenv`).

- **`doc_formater.py`**  
  Генерация DOCX‑отчёта на базе `docxtpl`:
  - Константы:
    - `TEMPLATE_PATH = template/template.docx`
    - `OUTPUT_DIR = output`
  - `doc_render(context, filename='Topics.docx')`:
    - проверяет наличие шаблона;
    - рендерит документ по контексту;
    - создаёт каталог `output` (если его ещё нет);
    - сохраняет итоговый файл.

- **`models.py`**  
  Pydantic‑модели для данных ВК:
  - `Comments`:
    - поля:
      - `date: datetime` — через валидатор переводит Unix‑timestamp во `datetime` и сериализует в строку `'%d.%m.%Y'` при экспорте;
      - `text: str` — текст комментария.
  - `Topic`:
    - поля:
      - `title: str` — заголовок темы;
      - `comments: list[Comments]` — список комментариев темы.

- **`logger_setup.py`**  
  Единообразная настройка логирования:
  - `setup_logger(level, name, log_file=None) -> logging.Logger`:
    - настраивает логгер с выводом в stdout;
    - по желанию добавляет FileHandler, если передан `log_file`;
    - использует формат: `'%(asctime)s %(name)s [%(levelname)s] %(message)s'` и дату `'%d.%m.%Y %H:%M'`.

- **`template/template.docx`**  
  Шаблон отчёта Word для библиотеки `docxtpl`.  
  В шаблоне вы можете использовать переменные из контекста. По умолчанию в `main.py` передаётся:

  ```python
  context = {
      "topics": [topic.model_dump(exclude=None) for topic in topics]
  }
  ```

  Структура контекста (пример):

  ```python
  [
      {
          "title": "Название темы",
          "comments": [
              {"date": "01.01.2024", "text": "Текст комментария 1"},
              {"date": "02.01.2024", "text": "Текст комментария 2"},
              ...
          ]
      },
      ...
  ]
  ```

  Пример Jinja‑разметки в шаблоне:

  ```jinja2
  {% for topic in topics %}
  {{ topic.title }}

  {% for comment in topic.comments %}
  {{ comment.date }} — {{ comment.text }}
  {% endfor %}

  {% endfor %}
  ```

- **`output/`**  
  Папка для сохранения сгенерированных документов (создаётся автоматически при первом запуске).

### Логирование

Логи настраиваются через `logger_setup.setup_logger` и используются во всех ключевых модулях (`main.py`, `vk_service.py`, `doc_formater.py`):

- по умолчанию выводятся в stdout;
- при желании можно передать путь к лог‑файлу в `setup_logger(log_file='logs/app.log')` в нужных местах.

Пример типичных сообщений:

- запуск основной функции;
- запуск запроса тем и комментариев;
- рендер документа;
- ошибки VK API и файловой системы.

### Возможные ошибки

- **`ValueError: Задайте переменные окружения ACCESS_TOKEN и GROUP_ID.`**  
  Не заданы или некорректно заданы переменные окружения. Проверьте файл `.env`.

- **`vk_api.VkApiError`**  
  Ошибка VK API:
  - неверный/просроченный токен;
  - недостаточные права доступа;
  - неверный `GROUP_ID`.

- **`FileNotFoundError: Шаблон не найден: template/template.docx`**  
  В папке `template` отсутствует файл `template.docx`. Убедитесь, что шаблон скопирован/создан и имеет нужное имя.

### Лицензия
MIT

### Автор
[Danil Zheltikov](https://github.com/DanilZheltikov)