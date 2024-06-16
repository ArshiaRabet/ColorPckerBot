import json
import logging

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    await update.message.reply_text(
'''سلام خوش آمديد! 😁
  براي استفاده از برنامه روی دکمه ی زیر کلیک کرده و برنامه را باز کنيد 👀 این بات توسط @Arshia_Rabet ساخته شده است ''',
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Open the color picker!",
                web_app=WebAppInfo(url="https://python-telegram-bot.org/static/webappbot"),
            )
        ),
    )


# Handle incoming WebAppData
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the received data and remove the button."""
    # Here we use `json.loads`, since the WebApp sends the data JSON serialized string
    # (see webappbot.html)
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_html(
        text=(
            f"کد HEX رنگ انتخابي شما : <code>{data['hex']}</code>"
         f" و کد RGB آن : <code>{tuple(data['rgb'].values())}</code> مي باشد"
        ),
        reply_markup=ReplyKeyboardRemove(),
    )


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("YOUR TOKEN").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()





    
