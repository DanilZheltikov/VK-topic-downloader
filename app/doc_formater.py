from typing import Any, Mapping

from docxtpl import DocxTemplate

from logger_setup import setup_logger
from settings import OUTPUT_DIR, TEMPLATE_PATH

logger = setup_logger(name=__name__)


def doc_render(
    context: Mapping[str, Any],
    filename: str = 'Topics.docx'
) -> None:
    """Рендерит DOCX из контекста по шаблону и сохраняет файл."""
    logger.info(f'Рендер документа: {filename}')
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f'Шаблон не найден: {TEMPLATE_PATH}')

    doc = DocxTemplate(TEMPLATE_PATH)
    doc.render(context)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    doc.save(OUTPUT_DIR / filename)
