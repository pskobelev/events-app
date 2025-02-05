import logging
from datetime import datetime

logger = logging.getLogger(__name__)


async def edit_msg(event_data):
    logger.debug("Editing message")
    logger.debug("Event data: %s", event_data)
    # Формируем текст для обновленного сообщения
    playing = [
        user["username"]
        for user in event_data
        if user["user_choice"] == "uc_in_game"
    ]
    thinking = [
        user["username"]
        for user in event_data
        if user["user_choice"] == "uc_thinking"
    ]
    not_playing = [
        user["username"]
        for user in event_data
        if user["user_choice"] == "uc_pass"
    ]
    logger.debug(
        "PLAYING: %s | THINKING: %s | NOT_PLAYING: %s",
        playing,
        thinking,
        not_playing,
    )

    message_text = f"""
Основной состав: {len(playing)} / 10:
{format_players_list(playing)}
Скамейка: {len(thinking)}:
{format_players_list(thinking)}
Не играют - {len(not_playing)}:
{format_players_list(not_playing)}
        """
    return message_text


async def format_date_with_day(event_date):
    date = datetime.fromisoformat(event_date)
    date_with_day = f"🗓️{date.date().isoformat()} ({date.strftime('%A')})"
    return date_with_day


def format_players_list(players: list, prefix: str = "") -> str:
    if not players:
        return prefix + "Пусто"

    # Нумеруем игроков с 1 и добавляем перенос строки
    return (
            prefix
            + "\n"
            + "\n".join(
        f"👟{i + 1}. {player}" for i, player in enumerate(players))
    )
