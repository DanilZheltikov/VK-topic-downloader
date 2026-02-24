# VK Topic Downloader

Инструмент для выгрузки тем и комментариев из обсуждений сообщества ВКонтакте и генерации DOCX-отчёта по шаблону.

## Возможности

* загрузка тем обсуждений сообщества;
* выгрузка всех комментариев с пагинацией;
* преобразование данных через Pydantic-модели;
* генерация DOCX-отчёта через шаблон (`docxtpl`);
* логирование процесса выполнения.

## Требования

* Python 3.11+
* vk-api
* python-dotenv
* pydantic v2
* docxtpl

Установка зависимостей:

```bash
pip install -r requirements.txt
```

## Установка

```bash
git clone https://github.com/DanilZheltikov/VK-topic-downloader.git
cd VK-topic-downloader

python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
```

## Настройка

Создайте файл `.env` в корне проекта:

```env
ACCESS_TOKEN=ваш_vk_токен
GROUP_ID=123456789
```

* **ACCESS_TOKEN** — токен доступа с правами на чтение обсуждений.
* **GROUP_ID** — ID сообщества (без минуса).

## Запуск

```bash
python main.py
```

После выполнения будет создан файл:

```
output/Topics.docx
```

## Структура проекта

* `main.py` — точка входа.
* `vk_service.py` — работа с VK API.
* `doc_formater.py` — генерация DOCX по шаблону.
* `models.py` — Pydantic-модели.
* `logger_setup.py` — настройка логирования.
* `template/template.docx` — шаблон документа.
* `output/` — сгенерированные файлы.

## Шаблон DOCX

В шаблон передаётся контекст:

```python
{
    "topics": [
        {
            "title": "Название темы",
            "comments": [
                {"date": "01.01.2024", "text": "Комментарий"}
            ]
        }
    ]
}
```

Пример разметки шаблона:

```jinja2
{% for topic in topics %}
{{ topic.title }}

{% for comment in topic.comments %}
{{ comment.date }} — {{ comment.text }}
{% endfor %}

{% endfor %}
```

## Возможные ошибки
* ошибка API VK
* отсутствуют переменные окружения `.env`;
* неверный токен или `GROUP_ID`;
* отсутствует `template/template.docx`.

## Лицензия

MIT

## Автор

[Danil Zheltikov](https://github.com/DanilZheltikov)
