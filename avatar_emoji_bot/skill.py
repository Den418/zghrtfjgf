import asyncio

from folds import Skill, Message, SystemMessage
from telethon import Button, client

from avatar_emoji_bot.functions import update_or_create_set
from avatar_emoji_bot.utils import get_chat_set_link
from telethon import events
import json
from pathlib import Path

skill = Skill()
lock = asyncio.Lock()


@skill.added_to_group()
async def f(event: SystemMessage):
    chat_id = event.chat.id

    # if chat_id not in ALLOWED_CHATS:
    #     return await event.respond("⚠️ Эта группа не имеет доступа к обновлению эмодзи паков.")

    await event.respond('Создаю эмодзи пак... Минутку!')

    user_id = event.original_update.new_participant.inviter_id
    async with lock:
        is_created = await update_or_create_set(event.chat, user_id)

    if is_created:
        return f'Готово!\n{get_chat_set_link(event)}'
    else:
        return f'Пак обновлён!\n{get_chat_set_link(event)}'



@skill.group_commands.update()
async def f(message: Message):
    info_message = await message.respond('Обновление пака... Мгновение!')

    async with lock:
        await update_or_create_set(message.chat, message.sender_id)

    await info_message.reply(f'Пак обновлён!\n{get_chat_set_link(message)}')


@skill.private_message()
async def f(message: Message):
    # button = Button.url('Выберите группу', f't.me/{message.client.me.username}?startgroup')
    button = [
        [
            Button.url(
                'Выберите группу',
                f't.me/{message.client.me.username}?startgroup'
            )
        ],
        [
            Button.url(
                'Поддержать на Boosty',
                'https://boosty.to/den418dev'
            )
        ]
    ]
    await message.respond(
        "👋 Привет!\n\n"
        "Добавьте меня в группу, чтобы создать ваш собственный пакет эмодзи! 🎨\n\n"
        "После добавления вы можете использовать команду `/update` для обновления набора эмодзи, если кто-то новый присоединится к чату.\n\n"
        "Проект полностью бесплатный, поэтому если вам нравится, пожалуйста, поддержите нас! 💖",
        buttons=button
    )


ALLOWED_CHATS_FILE = Path("allowed_chats.json")

def load_allowed_chats():
    if ALLOWED_CHATS_FILE.exists():
        with open(ALLOWED_CHATS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_allowed_chats(chats):
    with open(ALLOWED_CHATS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(chats), f, ensure_ascii=False, indent=2)

# ALLOWED_CHATS = load_allowed_chats()
#
# ADMINS = {123456789}  # сюда добавь ID своего аккаунта Telegram
#
# @client.on(events.NewMessage(pattern='/allow_chat'))
# async def allow_chat(event):
#     if event.sender_id not in ADMINS:
#         return await event.respond("🚫 У вас нет прав на эту команду.")
#
#     chat_id = event.chat.id
#     ALLOWED_CHATS.add(chat_id)
#     save_allowed_chats(ALLOWED_CHATS)
#     await event.respond("✅ Эта группа теперь привилегированная. Обновления пакета разрешены.")
#
# @client.on(events.NewMessage(pattern='/disallow_chat'))
# async def disallow_chat(event):
#     if event.sender_id not in ADMINS:
#         return await event.respond("🚫 У вас нет прав на эту команду.")
#
#     chat_id = event.chat.id
#     ALLOWED_CHATS.discard(chat_id)
#     save_allowed_chats(ALLOWED_CHATS)
#     await event.respond("❌ Эта группа больше не привилегированная.")
#
# @client.on(events.NewMessage(pattern='/list_chats'))
# async def list_chats(event):
#     if event.sender_id not in ADMINS:
#         return await event.respond("🚫 У вас нет прав на эту команду.")
#
#     if not ALLOWED_CHATS:
#         return await event.respond("Пока нет привилегированных групп.")
#
#     text = "Привилегированные группы:\n" + "\n".join(str(c) for c in ALLOWED_CHATS)
#     await event.respond(text)


