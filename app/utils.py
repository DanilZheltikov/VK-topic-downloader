from datetime import datetime


def timestamp_to_date(timestamp: int) -> str:
    """Переводит время из timestamp в понятный формат."""
    date = datetime.fromtimestamp(timestamp)
    return date.strftime('%d.%m.%Y')
