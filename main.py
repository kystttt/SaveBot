import logging
import uvicorn
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from telegram import Update
from my_settings_env import APP_URL, WEBHOOK_PATH
from my_bot_core.bot import app_telegram



@asynccontextmanager
async def lifespan(app: FastAPI):
    url = APP_URL + WEBHOOK_PATH
    logging.info(f"Starting with {url}")
    await app_telegram.initialize()
    logging.info(f"Запустили бота {url}")
    await app_telegram.bot.set_webhook(url)
    logging.info(f"Webhook установлен: {url}")
    try:
        yield
    finally:
        logging.info("Завершаем приложение. Удаляем Webhook.")
        await app_telegram.bot.delete_webhook()
        await app_telegram.shutdown()
        logging.info("Уложили бота спать")
app = FastAPI(lifespan=lifespan)

@app.post(WEBHOOK_PATH)
async def receive_update(request: Request):
    data = await request.json()
    logging.info("Получен update: %s", data)
    update = Update.de_json(data, app_telegram.bot)
    await app_telegram.process_update(update)
    return {"ok": True}
@app.get("/")
async def read_root():
    return {"msg": "Bot is alive"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8080)