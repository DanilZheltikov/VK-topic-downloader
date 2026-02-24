import os
from typing import Any, Callable, Generator

import vk_api
from dotenv import load_dotenv

from logger_setup import setup_logger
from models import Comments, Topic

logger = setup_logger(name=__name__)

load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
GROUP_ID = int(os.getenv('GROUP_ID')) if os.getenv('GROUP_ID') else None


def paginate_response(
    method: Callable[..., dict[str, Any]],
    **params: Any
) -> Generator[dict[str, Any], None, None]:
    """Универсальная пагинация для VK API."""
    count = 100
    offset = 0

    while True:
        response = method(count=count, offset=offset, **params)
        items = response.get('items', [])

        if not items:
            break

        yield from items

        offset += count


def get_title_and_id_from_topics(
    vk: vk_api.vk_api.VkApiMethod,
    group_id: int
) -> dict[int, str]:
    """
    Получает все обсуждения группы и возвращает словарь: {topic_id: title}
    """
    logger.info(f'Запрос топиков группы {group_id}')

    return {
        item['id']: item['title']
        for item in paginate_response(vk.board.getTopics, group_id=group_id)
    }


def get_all_comments(
    vk: vk_api.vk_api.VkApiMethod,
    group_id: int,
    topic_id: int
) -> list[Comments]:
    """Отдает все комментарии топика."""
    logger.info(f'Запрос комментов топика {topic_id}')
    return [
        Comments(**item)
        for item in paginate_response(
            vk.board.getComments,
            group_id=group_id,
            topic_id=topic_id
        )
    ]


def get_topics_with_comments(
    token: str = ACCESS_TOKEN,
    group_id: int = GROUP_ID
) -> list[Topic]:
    """Собирает и отдает список топиков с коментариями."""
    logger.info('Сбор топиков и комментариев в один список')
    if not token or not group_id:
        raise ValueError(
            'Задайте переменные окружения ACCESS_TOKEN и GROUP_ID.'
        )
    try:
        vk_session = vk_api.VkApi(token=token)
        vk = vk_session.get_api()

        topics = []
        titles = get_title_and_id_from_topics(vk, group_id)

        for title_id, title in titles.items():
            logger.info(f'Запрос коментов топика {title}')

            comments = get_all_comments(vk, group_id, title_id)
            topics.append(
                Topic(
                    title=title,
                    comments=comments
                )
            )
        return topics

    except vk_api.VkApiError:
        raise
