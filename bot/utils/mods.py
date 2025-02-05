import json
import re
from datetime import datetime


async def format_text(msg):
    return json.dumps(msg, ensure_ascii=False, indent=2)


async def handle_response(resp):
    """
    Handle and format response from server
    """
    if resp.status == 200:
        data = await resp.json()
        return data
    else:
        error_data = await resp.json()
        error_text = await format_text(error_data)
        raise ValueError(
            f"Server responded with an error: {resp.status}, {error_text}"
        )


async def extract_datetime(text):
    # Шаблон для поиска даты и времени в формате YYYY-MM-DD HH:MM или только даты YYYY-MM-DD
    pattern = r"\b(\d{4}-\d{2}-\d{2})(?: (\d{2}:\d{2}))?\b"
    match = re.search(pattern, text)
    if match:
        date_part = match.group(1)  # Всегда есть дата
        time_part = (
                match.group(2) or "10:30"
        )  # Подставляем стандартное время, если его нет
        datetime_str = f"{date_part} {time_part}"
        try:
            return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Неверный формат даты")
    else:
        return None
