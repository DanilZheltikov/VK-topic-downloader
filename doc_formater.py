from pathlib import Path
from typing import Any, Mapping

from docxtpl import DocxTemplate

from logger_setup import setup_logger

logger = setup_logger(name=__name__)

BASE_DIR = Path(__file__).parent
TEMPLATE_PATH = BASE_DIR / 'template' / 'template.docx'
OUTPUT_DIR = BASE_DIR / 'output'


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
