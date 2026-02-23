from sys import exit

from doc_formater import doc_render
from logger_setup import setup_logger
from vk_service import get_topics_with_comments

logger = setup_logger(name=__name__)


def main():
    """Управляющая функция."""
    logger.info('Запуск основной функции.')
    try:
        topics = get_topics_with_comments()
        context = {
            'topics': [topic.model_dump(exclude=None) for topic in topics]
        }
        doc_render(context=context)

    except Exception as error:
        logger.error(f'Ошибка: {error}')
        exit()


if __name__ == '__main__':
    main()
