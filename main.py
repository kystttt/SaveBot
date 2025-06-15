import logging
from pathlib import Path
import uvicorn
import asyncio
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from telegram import Update
from my_settings_env import APP_URL, WEBHOOK_PATH
from my_bot_core.bot import app_telegram
from my_helping_functions import download_video
from urllib.parse import quote_plus


@asynccontextmanager
async def lifespan(app: FastAPI):
    url = APP_URL + WEBHOOK_PATH
    await app_telegram.initialize()
    logging.info(f"Запустили бота")
    await app_telegram.bot.set_webhook(url)
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

@app.post("/download")
async def download_file(file_link: dict):
    """
    Ручка, которая позволяет скачивать видео
    """
    url = file_link["url"]
    safe_url = quote_plus(url)
    project_path = Path(__file__).resolve().parent
    temp_path = project_path / "tmp"
    video_path = temp_path / f'{safe_url}.mp4'
    if not video_path.exists():
        path = await asyncio.get_event_loop().run_in_executor(None, download_video, url)
    else:
        path = str(video_path)
    return {"path": path}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8080)