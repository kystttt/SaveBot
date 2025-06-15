import logging
from telegram.ext import Application
from my_bot_core.my_bot_handler import BotLogicHandler
from telegram.ext import CommandHandler, MessageHandler, filters
from my_settings_env import BOT_TOKEN


logging.basicConfig(level=logging.INFO)
logic = BotLogicHandler()
app_telegram = Application.builder().token(BOT_TOKEN).build()
app_telegram.add_handler(CommandHandler('start', logic.start))
app_telegram.add_handler(CommandHandler('help', logic.help))
app_telegram.add_handler(
    MessageHandler(
        filters.TEXT &
        filters.Regex("^https:\/\/www\.tiktok\.com\/t\/\S*") &
        (~filters.UpdateType.EDITED), logic.reply_video))
app_telegram.add_handler(
    MessageHandler(
        filters.TEXT &
        (filters.Regex("^https:\/\/vkvideo\.ru.*") |
         filters.Regex("^https:\/\/vk\.com\/video.*")) &
        (~filters.UpdateType.EDITED), logic.reply_video))
app_telegram.add_handler(
    MessageHandler(
        filters.TEXT &
        ~filters.Regex("^https:\/\/www\.tiktok\.com\/t\/\S*"), logic.error)
)
