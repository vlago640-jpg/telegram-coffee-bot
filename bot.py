import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="☕ Меню кофейни", callback_data="menu")],
            [InlineKeyboardButton(text="📍 Адрес и часы", callback_data="address")],
            [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")],
            [InlineKeyboardButton(text="📝 Оставить заявку", callback_data="order")],
        ]
    )


@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        f"Я бот кофейни <b>Bean There</b>.\n"
        f"Выбери, что тебя интересует:"
    )
    await message.answer(text, reply_markup=main_menu(), parse_mode="HTML")


@dp.callback_query(F.data == "menu")
async def show_menu(callback: CallbackQuery):
    text = (
        "<b>☕ Наше меню</b>\n\n"
        "• Эспрессо — 150 ₽\n"
        "• Капучино — 220 ₽\n"
        "• Латте — 240 ₽\n"
        "• Раф ванильный — 280 ₽\n"
        "• Какао — 200 ₽\n\n"
        "🥐 Круассан — 150 ₽\n"
        "🍰 Чизкейк — 280 ₽"
    )
    await callback.message.answer(text, reply_markup=main_menu(), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "address")
async def show_address(callback: CallbackQuery):
    text = (
        "<b>📍 Где нас найти</b>\n\n"
        "г. Москва, ул. Кофейная, 5\n"
        "🕘 Пн–Пт: 8:00 – 22:00\n"
        "🕙 Сб–Вс: 10:00 – 23:00"
    )
    await callback.message.answer(text, reply_markup=main_menu(), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "contacts")
async def show_contacts(callback: CallbackQuery):
    text = (
        "<b>📞 Связаться с нами</b>\n\n"
        "Телефон: +7 (999) 123-45-67\n"
        "Instagram: @beanthere\n"
        "Email: hi@beanthere.ru"
    )
    await callback.message.answer(text, reply_markup=main_menu(), parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "order")
async def show_order(callback: CallbackQuery):
    text = (
        "📝 <b>Оставить заявку</b>\n\n"
        "Напиши сообщением, что ты хочешь заказать, "
        "и мы свяжемся с тобой в течение 10 минут."
    )
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()


@dp.message(F.text)
async def handle_text(message: Message):
    await message.answer(
        "✅ Спасибо! Заявка принята, мы свяжемся с тобой.",
        reply_markup=main_menu(),
    )


async def main():
    print("Бот запущен ✅")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
