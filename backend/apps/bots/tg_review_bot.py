"""
This bot is created for the demonstration of a usage of inline keyboards.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types
from django.conf import settings
from post.models import Post, Reviewer
from image.utils import get_raw_image

API_TOKEN = settings.TELEGRAM_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def get_keyboard_markup():
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    text_and_data = (
        ('➡️', 'next'),
        ('👍', 'up_vote'),
    )
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)

    return keyboard_markup


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    await message.reply("Lets_start", reply_markup=get_keyboard_markup())


@dp.callback_query_handler(text='up_vote')
async def up_vote(query: types.CallbackQuery):
    await query.answer(f'Good choice')
    post_tg_id = query.message.message_id
    post = Post.objects.get(reviewed_by__post_tg_id=post_tg_id)
    post.reviewed_rating += 1
    post.save()


def _get_post(user_id):
    post = Post.objects.filter(on_review=False).first()

    if not post:
        return Post.objects.exclude(reviewed_by__user_id=user_id).first()

    return post


@dp.callback_query_handler(text='next')
async def get_post(query: types.CallbackQuery):
    await query.answer(f'Looking for memes...')
    post = _get_post(query.from_user.id)

    if not post:
        await bot.send_message(
            query.from_user.id,
            'You reached the infinite limit, wait a little, then get next',
            reply_markup=get_keyboard_markup()
        )
        return

    image = post.images.first()

    with get_raw_image(image) as raw_image:
        answ = await bot.send_photo(query.from_user.id, raw_image, reply_markup=get_keyboard_markup())

    tg_id = answ.message_id
    full_name = answ.chat.full_name
    user_id = answ.chat.id

    reviewer = Reviewer.objects.create(
        user_id=user_id,
        post_tg_id=tg_id,
        full_name=full_name,
    )
    post.reviewed_by.add(reviewer)
    post.on_review = True
    post.save()


def main():
    executor.start_polling(dp, skip_updates=True)
