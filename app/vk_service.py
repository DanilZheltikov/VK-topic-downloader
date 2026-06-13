import asyncio
from http import HTTPStatus
from typing import Any

import aiohttp

from exceptions import InvalidAPIResponseError, VKApiError
from logger_setup import setup_logger
from settings import (
    COMMENT_METHOD,
    DEFAULT_OFFSET,
    DEFAULT_PARAMS,
    EMPTY_COMMENTS,
    EMPTY_TOPICS,
    HEADERS,
    ITEMS_COUNT,
    SEMAPHORE,
    TOPIC_METHOD,
    URL
)
from typed_dicts import Comment, Topic, TopicWithIDDict

logger = setup_logger(name=__name__)


async def make_vk_api_request(
    session: aiohttp.ClientSession,
    url: str,
    params: dict
) -> dict[str, Any]:
    """Выполняет асинхронный GET-запрос к VK API с валидацией ответа."""
    async with SEMAPHORE:
        async with session.get(
            url,
            params=params,
            headers=HEADERS
        ) as response:
            logger.debug(f'Запрос {url}, c параметрами {params}')

            if response.status != HTTPStatus.OK:
                raise InvalidAPIResponseError(
                    f'Не ожиданный статус-код: {response.status}'
                )

            vk_api_response: dict = await response.json()

            if 'error' in vk_api_response:
                raise VKApiError(
                    f'{vk_api_response['error']['error_msg']}\n'
                    f'Код ошибки: {vk_api_response['error']['error_code']}'
                )

            return vk_api_response.get('response', {})


async def paginate_response(
    session: aiohttp.ClientSession,
    total_items_count: int,
    method: str,
    topic_id: int | None = None,
) -> list:
    """Собирает элементы из всех страниц выборки через асинхронные запросы."""
    url = URL + method

    params = DEFAULT_PARAMS.copy()
    params.update({'count': ITEMS_COUNT})

    if topic_id:
        params.update({'topic_id': topic_id})

    tasks = []
    for offset in range(DEFAULT_OFFSET, total_items_count, ITEMS_COUNT):
        current_params = params.copy()
        current_params['offset'] = offset
        tasks.append(make_vk_api_request(session, url, current_params))

    responses = await asyncio.gather(*tasks)

    items = []
    for data in responses:
        if data and 'items' in data:
            items.extend(data['items'])

    return items


async def get_all_comments(
    session: aiohttp.ClientSession,
    topic: TopicWithIDDict
) -> list[Comment]:
    """Скачивает все комментарии из указанного обсуждения VK."""
    logger.info(f"Запрос комментариев обсуждения: {topic['title']}")
    return await paginate_response(
        session=session,
        total_items_count=topic['comments'],
        method=COMMENT_METHOD,
        topic_id=topic['id']
    )


async def get_topic_with_comments(
    session: aiohttp.ClientSession,
    topic: TopicWithIDDict
) -> Topic:
    """Формирует структуру обсуждения со всеми его комментариями."""
    comments = await get_all_comments(session, topic)
    if not comments:
        logger.debug('Комментариев нет.')
        comments = EMPTY_COMMENTS

    return {
        'title': topic['title'],
        'comments': comments
    }


async def get_all_topics_with_comments(
    session: aiohttp.ClientSession
) -> list[Topic]:
    """Получает все обсуждения сообщества вместе с их комментариями."""
    first_response = await make_vk_api_request(
        session=session,
        url=URL + TOPIC_METHOD,
        params=DEFAULT_PARAMS
    )
    total_topics_count = first_response.get('count', 0)
    if not total_topics_count:
        logger.debug('Обсуждений нет.')
        return EMPTY_TOPICS

    topics: list[TopicWithIDDict] = await paginate_response(
        session=session,
        total_items_count=total_topics_count,
        method=TOPIC_METHOD
    )

    tasks = [
        get_topic_with_comments(session, topic)
        for topic in topics
    ]

    return await asyncio.gather(*tasks)
