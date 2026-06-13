import asyncio
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).parent.parent
TEMPLATE_PATH = BASE_DIR / 'template' / 'template.docx'
OUTPUT_DIR = BASE_DIR / 'output'

TOKEN = config('TOKEN')
HEADERS = {'Authorization': f'Bearer {TOKEN}'}
URL = 'https://api.vk.ru/'
GROUP_ID = config('GROUP_ID')
VERSION = "5.199"
TOPIC_METHOD = 'method/board.getTopics'
COMMENT_METHOD = 'method/board.getComments'

REQUEST_PER_SECOND_COUNT = 6
SEMAPHORE = asyncio.Semaphore(REQUEST_PER_SECOND_COUNT)

ITEMS_COUNT = 100
DEFAULT_OFFSET = 0
DEFAULT_PARAMS = {
    'group_id': GROUP_ID,
    'v': VERSION,
    'count': 1,
    'offset': DEFAULT_OFFSET
}
