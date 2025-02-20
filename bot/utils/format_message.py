import logging
from datetime import datetime

from aiogram.utils.formatting import (
    Bold,
    as_marked_section, Text,
)

logger = logging.getLogger(__name__)


async def edit_msg(event_data) -> list:
    categories = {
        "Основной состав:": ("IN_GAME", "👟 "),
        "Скамейка:":        ("THINKING", "🔁 "),
        "Отказались:":      ("PASS", "❌ "),
    }

    content = []
    for category_name, (status, emoji) in categories.items():
        players = []
        for player in event_data:
            if player.get("user_choice") == status:
                player_name = player.get("username", "Unknown")
                players.append(f"{emoji}{player_name}")
        if players:
            section = as_marked_section(
                Bold(category_name), *players, marker=emoji
            ).as_kwargs()
            content.append(section)
    logger.debug("CONTENT: %s", content)
    return content


async def format_date_with_day(event_date):
    date = datetime.fromisoformat(event_date)
    date_with_day = f"🗓️ {date.date().isoformat()} ({date.strftime('%A')})"
    return date_with_day
