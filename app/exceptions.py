class VKApiError(Exception):
    """Общее исключение для ошибок api vk."""


class InvalidAPIResponseError(VKApiError):
    """Исключение для ответа не соответствующему ожидаемому."""
