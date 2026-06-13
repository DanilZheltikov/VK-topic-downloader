import asyncio
from sys import exit

import aiohttp
from doc_formater import doc_render
from logger_setup import setup_logger
from vk_service import get_all_topics_with_comments

logger = setup_logger(name=__name__)


async def main():
    """Управляющая функция."""
    logger.info('Запуск основной функции.')
    try:
        async with aiohttp.ClientSession() as session:
            topics = await get_all_topics_with_comments(session)

        context = {
            'topics': topics
        }
        doc_render(context=context)

        logger.info('Документ готов.')

    except Exception as error:
        logger.error(f'Ошибка: {error}')
        exit()


if __name__ == '__main__':
    asyncio.run(main())
