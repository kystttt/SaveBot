from telegram import Update
from telegram.ext import ContextTypes
from my_bot_core.my_bot_repl_constants import *
import httpx
from my_helping_functions import delete_file
from pathlib import Path
import time


class BotLogicHandler:
    """
    Класс, где реализована логика бота
    """

    def __init__(self):
        self.reply_kd = {}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    async def reply_video(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Получает ссылку на видео, в случае, если проблемы с доступом к видео
        (невалидная ссылка или еще что-то), то возвращает сообщение ERROR_VIDEO_EXC
        об ошибке, в случае успеха отправляет пользователю видео, и удаляет его с устройства.
        Также есть антиспам проверка, нельзя скачивать видео чаще, чем раз в 10 секунд.
        """
        video_url = update.message.text
        try:
            now_kd_time = time.monotonic()
            if update.message.chat_id in self.reply_kd:
                if now_kd_time - self.reply_kd.get(update.message.chat_id) < 10:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=BE_SLOW_REPLY
                    )
                    return
                self.reply_kd[update.message.chat_id] = time.monotonic()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8080/download",
                    json={"url": video_url},
                    timeout=300.0)
                response.raise_for_status()
            json_data = response.json()
            file_path = Path(json_data['path'])

            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=file_path.open("rb"),
                text=TG_BOT_ID
            )
            self.reply_kd[update.message.chat_id] = time.monotonic()
            delete_file(file_path)
        except Exception:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=ERROR_VIDEO_EXC
            )

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
