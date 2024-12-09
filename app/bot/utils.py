import json


async def format_text(msg):
    return json.dumps(msg, ensure_ascii=False, indent=2)


async def handle_response(resp):
    """
    Handle and format response from server
    """
    if resp.status == 200:
        data = await resp.json()
        return await format_text(data)
    else:
        error_data = await resp.json()
        error_text = await format_text(error_data)
        raise ValueError(
            f"Server responded with an error: {resp.status}, {error_text}"
        )
