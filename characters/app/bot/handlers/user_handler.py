import aiohttp
from aiogram import types
from app.bot.dispatcher import dp, bot
from app.api import crud, schemas, deps
from app.database.session import db
from app.core.config import settings
from app.bot.utils import amplitude

web_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
button = types.KeyboardButton(
    text="WebApp", web_app=types.WebAppInfo(url=settings.WEB_APP_URL)
)
web_markup.add(button)

headers = {"accept": "application/json", "Content-Type": "application/json"}

GPT_MODEL = "gpt-3.5-turbo"

user_conversations = {}


@dp.message_handler(commands=["start"])
async def start(message: types.Message) -> None:
    username = message.chat.username
    user = crud.user.get_by_username(db=db, username=username)
    amplitude.send_to_amplitude(event_type="User sign up")
    if not user:
        user_in = schemas.UserCreate(
            username=username,
            name=message.chat.first_name,
            surename=message.chat.last_name,
        )
        crud.user.create(db=db, obj_in=user_in)

    await message.answer(
        text="This bot do many interesting things", reply_markup=web_markup
    )


@dp.message_handler(commands=["menu"])
async def menu(message: types.Message) -> None:
    username = message.chat.username
    user = crud.user.get_by_username(db=db, username=username)
    if user:
        await message.answer(
            text="You can choose another character", reply_markup=web_markup
        )


@dp.message_handler(content_types=["web_app_data"])
async def web_app(message: types.Message):
    await message.answer("I'm thinking...")
    name = message.web_app_data.data
    char = crud.character.get_by_name(db=db, name=name)
    user_id = message.chat.id
    amplitude.send_to_amplitude(event_type=f"User choose the {name}")
    user_conversations.clear()
    user_conversations[user_id] = [
        {"role": "system", "content": char.content},
        {"role": "user", "content": f"Hi, {char.name}!"},
    ]
    data = {"model": GPT_MODEL, "messages": user_conversations[user_id]}

    async with aiohttp.ClientSession() as current_session:
        async with current_session.post(
            settings.GPT_ENDPOINT_URL, headers=headers, json=data
        ) as response:
            if response.status == 200:
                response_data = await response.json()
                await message.answer(response_data["choices"][0]["message"]["content"])


@dp.message_handler()
async def get_user_messages(message: types.Message):
    await message.answer("I'm thinking...")
    user = crud.user.get_by_username(db=db, username=message.chat.username)
    if user:
        amplitude.send_to_amplitude(event_type="User send message")
        user_id = message.chat.id
        user_conversations[user_id].append({"role": "user", "content": message.text})
        data = {"model": GPT_MODEL, "messages": user_conversations[user_id]}
        async with aiohttp.ClientSession() as current_session:
            async with current_session.post(
                settings.GPT_ENDPOINT_URL, headers=headers, json=data
            ) as response:
                if response.status == 200:
                    response_data = await response.json()
                    answer = response_data["choices"][0]["message"]["content"]
                    await message.answer(answer)
                    amplitude.send_to_amplitude(event_type="Model answer")
                    message_in = schemas.MessageCreate(
                        question=message.text, answer=answer
                    )
                    crud.message.create_with_author(
                        db=db, obj_in=message_in, author_id=user.id
                    )
    else:
        await message.answer("/start before")
