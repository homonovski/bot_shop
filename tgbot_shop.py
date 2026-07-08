import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== ТОКЕН БЕРЁТСЯ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ =====
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан! Добавь переменную окружения BOT_TOKEN.")
# ===================================================

main_keyboard = ReplyKeyboardMarkup(
    [
        [KeyboardButton("𒂭 Открыть магазин")],
        [KeyboardButton("𒅒 Инструкция")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f" Привет, {user.first_name}!\n\n"
        "Я бот-магазин Homonovski Market. Здесь ты можешь заказать разработку ботов, сайтов и автоматизацию.\n\n"
        " Нажми на кнопку «𒂭 Открыть магазин», чтобы посмотреть услуги, или «𒅒 Инструкция».",
        reply_markup=main_keyboard
    )

async def open_shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "𒋲 Нажми на кнопку Open, чтобы перейти в каталог услуг.\n\n"
        "Если кнопка не отображается, обнови чат или перезапусти бота командой /start.",
        reply_markup=main_keyboard
    )

async def show_instruction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    instruction_text = (
        " ♛ **Как пользоваться магазином**\n\n"
        "1. Для корректного использования магазина включи VPN.\n"
        "2. Нажми на кнопку **«𒂭 Открыть магазин»** внизу экрана.\n"
        "3. Внутри мини-приложения выбери нужную услугу.\n"
        "4. Нажми **«Купить»** — оплата проходит через Юkassa/СБП.\n"
        "5. После оплаты ты получишь доступ к услуге.\n\n"
        "♛ Спасибо, что выбираете Homonovski Market."
    )
    await update.message.reply_text(instruction_text, parse_mode="Markdown", reply_markup=main_keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "𒂭 Открыть магазин":
        await open_shop(update, context)
    elif text == "𒅒 Инструкция":
        await show_instruction(update, context)
    else:
        await update.message.reply_text(
            "Используй кнопки внизу экрана или напиши /start.",
            reply_markup=main_keyboard
        )

def main():
    request = HTTPXRequest(proxy=None)
    app = Application.builder().token(BOT_TOKEN).request(request).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
