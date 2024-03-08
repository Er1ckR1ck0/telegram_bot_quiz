from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, FSInputFile, URLInputFile
import json
router = Router()

def add_person(id: str, name: str) -> None:
    try:
        with open('./info/persons.json', 'r') as file:
            data = json.load(file)
    except:
        data = {}
    if not id in data:
        data[id] = {"name": name, 'correct': 0, 'wrong': 0}
    with open('./info/persons.json', 'a') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    

@router.callback_query(lambda F: F.data in ["start_quiz"])
async def start_quiz(callback: CallbackQuery):
    add_person(callback.from_user.id, callback.from_user.full_name)
    await callback.message.answer(text='Ну что? Приступим')