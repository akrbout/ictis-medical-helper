import asyncio
import os

from fastapi import FastAPI
from src.database import create_db
from src.scaled_artificial_module import scaled_artificial_module
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from aiogram import Bot
from aiogram import types as aiogram_types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode, InputFile
from aiogram.utils import executor

app = FastAPI()

DATABASE_URL = os.environ["DB_CONNECTION_STRING"]
TELEGRAM_SECRET = os.environ["TELEGRAM_SECRET"]
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BOT = Bot(token=TELEGRAM_SECRET)
telegram_bot = Dispatcher(BOT)


@app.post("/get_prediction", description="Вводите симптомы на АНГЛИЙСКОМ ЯЗЫКЕ, "
                                         "без пробелов и через запятую (пробел заменяем на _underline_style_)")
async def get_prediction(symptoms: str):
    prediction = scaled_artificial_module(symptoms)
    return {"Prediction": prediction}


@telegram_bot.message_handler(commands=["predict"])
async def telegram_get_prediction(message: aiogram_types.Message):
    msg_txt = message.text.split(" ")
    if len(msg_txt) > 1:
        await message.answer(f"{message.from_user.first_name}, высчитываем диагноз, ожидайте, "
                             f"пожалуйста! Среднее время ответа: ±30 секунд")
        prediction = scaled_artificial_module(msg_txt[1])
        await message.answer(f"Возможный диагноз: {prediction}. Будьте осторожны и выздоравливайте!")
    else:
        await message.answer(f"Вы отправили пустую команду! Если Вы не знаете, как правильно взаимодействовать с ботом"
                             f", то отправьте команду '/help' для уточнения деталей.")


@telegram_bot.message_handler(commands=["help"])
async def telegram_helper(message: aiogram_types.Message):
    await message.answer("На данный момент доступны следующие команды:\n"
                         "/predict [список_симптомов через запятую без пробелов]")


@app.get("/health")
async def health_check():
    return {"Status": "OK"}


@app.on_event("startup")
async def on_startup():
    create_db()
    event_loop = asyncio.get_event_loop()
    event_loop.create_task(await telegram_bot.start_polling())
    app.state.db = SessionLocal()


@app.on_event("shutdown")
async def shutdown():
    app.state.db.close()
