from typing import Any

import jinja2
from docxtpl import DocxTemplate

from logger_setup import setup_logger
from settings import OUTPUT_DIR, TEMPLATE_PATH
from utils import timestamp_to_date

logger = setup_logger(name=__name__)


def doc_render(
    context: dict[str, Any],
    filename: str = 'Topics.docx'
) -> None:
    """Рендерит DOCX из контекста по шаблону и сохраняет файл."""
    logger.info(f'Рендер документа: {filename}')
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f'Шаблон не найден: {TEMPLATE_PATH}')

    jinja_env = jinja2.Environment()
    jinja_env.filters['timestamp_to_date'] = timestamp_to_date

    doc = DocxTemplate(TEMPLATE_PATH)
    doc.render(context, jinja_env=jinja_env)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT_DIR / filename)
