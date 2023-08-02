from asyncio import sleep 
from loader import bot

async def remove_message(chat_id: int, message_id: int, delay: int = 60) -> None:
    try:
        await sleep(delay)
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as ex:
        print(f"Попытка удаления уже отредактированooго сooбщения: \n {ex}")

