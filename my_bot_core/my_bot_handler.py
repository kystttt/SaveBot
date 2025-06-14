from telegram import Update
from telegram.ext import ContextTypes
from my_bot_core.my_bot_repl_constants import *

class BotLogicHandler:
    """
    Класс, где реализована логика бота
    """
    def __init__(self):
        pass

    async def start(self,update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Команда /start
        """
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=START_MESSAGE
        )

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Команда /help
        """
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=HELP_MESSAGE
        )
    async def tiktok(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Выдает ошибку, если пользователь отправил
        сообщение, которое не является командой или
        ссылкой на тикток
        """
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=ERROR_UNKNOWN_MESSAGE
        )