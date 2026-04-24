import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

load_dotenv()

from fpdf import FPDF

start_button = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Create PDF")]
    ],
    resize_keyboard=True
)

class PDFState(StatesGroup):
    filename = State()
    text = State()

TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=TOKEN)

dp = Dispatcher()


@dp.message(F.text == "/start")
async def start_cmd(msg: Message):
    await msg.reply("Hi Sir or Madam. Would you create a pdf?", reply_markup=start_button)

@dp.message(F.text == "Create PDF")
async def start_pdf(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("Well, how do you want to name this file? (end with .pdf)")
    await state.set_state(PDFState.filename)

@dp.message(PDFState.filename)
async def get_filename(msg: Message, state: FSMContext):
    if msg.text.endswith(".pdf"):
        await state.update_data(filename=msg.text)
    else: 
        name = f"{msg.text}.pdf"
        await state.update_data(filename=name)

    await msg.answer("Ok, Send me a text")
    await state.set_state(PDFState.text)

@dp.message(PDFState.text)
async def get_text(msg: Message, state: FSMContext):
    data = await state.get_data()

    text = msg.text
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(data.get("filename"))
    await msg.answer_document(FSInputFile(data.get('filename')), caption="Your PDF is ready✅")
    os.remove(data.get('filename'))
    await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Bot is ready!")
    asyncio.run(main())

