import os

import vk_api
from dotenv import load_dotenv

from logger_setup import setup_logger
from models import Comments, Topic

logger = setup_logger(name=__name__)

load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
GROUP_ID = int(os.getenv('GROUP_ID')) if os.getenv('GROUP_ID') else None


def get_all_comments(
    vk: vk_api.vk_api.VkApiMethod,
    group_id: int,
    topic_id: int
) -> list[Comments]:
    """Отдает все комментарии топика."""
    logger.info('Запрос комментов')
    offset = 0
    count = 100
    comments = []

    while True:
        response = vk.board.getComments(
            group_id=group_id,
            topic_id=topic_id,
            count=count,
            offset=offset
        )
        items = response['items']

        if not items:
            break

        comments.extend(Comments(**item) for item in items)
        offset += count

    return comments


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

        titles = {
            item['id']: item['title']
            for item in vk.board.getTopics(group_id=group_id)['items']
        }

        topics = []

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

    except vk_api.VkApiError as error:
        raise vk_api.VkApiError(f'Ошибка Апи: {error}')
