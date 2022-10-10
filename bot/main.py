import logging

from dotenv import dotenv_values, load_dotenv
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, Updater
from telegram.parsemode import ParseMode
from telegram.utils.request import Request


_logger = logging.getLogger(__name__)
load_dotenv()
config = dotenv_values("local.env")  # take environment variables from local.env files

TOKEN: str = config.get("TOKEN", "some_my_token")
PROXY_URL: str = config.get("PORT", None)

DESCRIPTION = """/help - Show help
/start - Start working"""


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f"Some error: {e}"
            _logger.error(error_message)
            raise e

    return inner


@log_errors
def show_help(update: Update, context: CallbackContext):
    update.message.reply_text(text=f"Supported commands:\n{DESCRIPTION}")


@log_errors
def start(update: Update, context: CallbackContext):
    """the callback for handling start command"""
    bot: Bot = context.bot
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello User, You have used <b>start</b> command for working with <b>YTEssence</b>.",
        parse_mode=ParseMode.HTML,
    )


if __name__ == "__main__":
    # 1 -- connections
    request = Request(connect_timeout=0.5, read_timeout=1.0)
    bot = Bot(request=request, token=TOKEN, base_url=PROXY_URL)
    _logger.info(bot.get_me())

    # 2 -- handles
    updater = Updater(bot=bot, use_context=True)

    # Add handlers for Telegram messages
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", show_help))

    # 3 -- Run processing loop of input messages
    updater.start_polling()
    updater.idle()
