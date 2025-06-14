import pytest
from unittest.mock import AsyncMock, MagicMock
from my_bot_core.my_bot_handler import BotLogicHandler
from datetime import datetime
from telegram import Update, Chat, User, Message

@pytest.mark.asyncio
class TestBotLogic:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.logic = BotLogicHandler()
        self.chat = Chat(id=123, type="private")
        self.user = User(id=456, first_name="TestUser", is_bot=False)
        self.message = Message(
            message_id=1,
            date=datetime.now(),
            chat=self.chat,
            from_user=self.user,
            text=""
        )
        self.update = Update(update_id=1, message=self.message)
        self.context = MagicMock()
        self.context.bot.send_message = AsyncMock()

    async def test_bot_reply_start(self):
        test_message = Message(
            message_id=1,
            date=datetime.now(),
            chat=self.chat,
            from_user=self.user,
            text="/start"
        )
        update = Update(update_id=1, message=test_message)
        await self.logic.start(self.update, self.context)
        self.context.bot.send_message.assert_awaited_once_with(
            chat_id=self.chat.id,
            text="Доброго времени суток!\nМожете отправить мне ссылку на видео в тикток и в ответ получите видео"
        )

    async def test_bot_reply_help(self):
        test_message = Message(
            message_id=3,
            date=datetime.now(),
            chat=self.chat,
            from_user=self.user,
            text="/help"
        )
        update = Update(update_id=3, message=test_message)
        await self.logic.help(self.update, self.context)
        self.context.bot.send_message.assert_awaited_once_with(
            chat_id=self.chat.id,
            text="Это бот для скачивания видео\n"
                "Отправьте ссылку на видео в тикток, для того, чтобы скачать\n\n\n"
                "Список доступных команд:\n"
                "/start - Выводит приветственное сообщение\n"
                "/help - Выводит список доступных команд")

    @pytest.mark.parametrize(
        "message_text, expected",
        [
        ("hee", "Ошибка! Такой команды нет!\n/help - для просмотра актуальных команд"),
        ("hi2121", "Ошибка! Такой команды нет!\n/help - для просмотра актуальных команд"),
        ]
    )
    async def test_bot_reply_error(self, message_text, expected):
        test_message = Message(
            message_id=2,
            date=datetime.now(),
            chat=self.chat,
            from_user=self.user,
            text=message_text
        )
        update = Update(update_id=2, message=test_message)
        await self.logic.error(update, self.context)
        self.context.bot.send_message.assert_awaited_once_with(
            chat_id=self.chat.id,
            text=expected
        )