import os

from vkwave.api import API
from vkwave.bots import SimpleBotEvent, SimpleLongPollBot
from vkwave.bots.core.dispatching import filters
from vkwave.bots.utils.keyboards import Keyboard
from vkwave.bots.utils.keyboards.keyboard import ButtonColor
from vkwave.bots.utils.uploaders import PhotoUploader
from vkwave.client import AIOHTTPClient

from . import crud
from .database import async_session

GROUP_ID = os.environ["GROUP_ID"]
TOKEN = os.environ["TOKEN"]

api = API(clients=AIOHTTPClient(), tokens=TOKEN)
uploader = PhotoUploader(api.get_context())
bot = SimpleLongPollBot(tokens=TOKEN, group_id=GROUP_ID)


@bot.message_handler(
    bot.text_contains_filter("начать")
    | bot.text_contains_filter("start")
    | filters.PayloadContainsFilter("start")
)
async def list_categories(event: SimpleBotEvent):
    '''Выводим перечень разделов'''

    async with async_session() as db:
        categories = await crud.get_categories(db)

    kb = Keyboard(one_time=True)
    for c in categories:
        kb.add_text_button(
            text=c.name,
            payload={
                "category_id": c.id,
                "back_stack": [{"start": True}]
            },
            color=ButtonColor.POSITIVE,
        )

    user_data = (await event.api_ctx.users.get(
        user_ids=event.object.object.message.peer_id
    )).response[0]

    await event.answer(
        message=f"Привет, {user_data.first_name}. Выбери раздел выпечки.",
        keyboard=kb.get_keyboard(),
    )


@bot.message_handler(filters.PayloadContainsFilter("category_id"))
async def list_products(event: SimpleBotEvent):
    '''Выводим перечень товаров'''

    category_id = event.payload["category_id"]
    back_stack = event.payload["back_stack"]

    async with async_session() as db:
        products = await crud.get_products(db, category_id)

    kb = Keyboard(one_time=True)
    for p in products:
        kb.add_text_button(
            text=p.name,
            payload={
                "product_id": p.id,
                "back_stack": [*back_stack, {"category_id": category_id}]
            },
            color=ButtonColor.POSITIVE,
        )

    kb.add_row()
    back_payload = {**back_stack[-1], "back_stack": back_stack[:-1]}
    kb.add_text_button(text="Назад", payload=back_payload)

    user_data = (await event.api_ctx.users.get(
        user_ids=event.object.object.message.peer_id
    )).response[0]

    await event.answer(
        message=f"{user_data.first_name}, выбери выпечку.",
        keyboard=kb.get_keyboard(),
    )


@bot.message_handler(filters.PayloadContainsFilter("product_id"))
async def show_product(event: SimpleBotEvent):
    '''Демонстрируем конкретный товар'''

    product_id = event.payload["product_id"]
    back_stack = event.payload["back_stack"]

    kb = Keyboard(one_time=True)
    back_payload = {**back_stack[-1], "back_stack": back_stack[:-1]}
    kb.add_text_button(text="Назад", payload=back_payload)

    async with async_session() as db:
        product = await crud.get_product(db, product_id)

    attachment = await uploader.get_attachment_from_path(
        peer_id=event.peer_id,
        file_path=f"images/{product.id}.jpg",
    )

    await event.answer(
        message=f"{product.name}\n{product.description}",
        attachment=attachment,
        keyboard=kb.get_keyboard(),
    )


if __name__ == '__main__':
    bot.run_forever()
