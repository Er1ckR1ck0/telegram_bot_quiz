from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, FSInputFile, URLInputFile
import json
router = Router()

def get_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='Запустить викторину', callback_data='start_quiz'))
    keyboard.adjust(1)
    return keyboard

def get_start_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text='Вернуться назад', callback_data='come_back'))
    keyboard.adjust(1)
    return keyboard

@router.callback_query(F.data == "come_back")
async def start(callback: CallbackQuery):
    keyboard = get_keyboard()
    await callback.message.answer(text='Приветствую!', reply_markup=keyboard.as_markup())
    await callback.answer(text='Я окошко')
    
@router.message(Command(commands=["start"]))
async def start(m: Message):
    keyboard = get_keyboard()
    await m.answer(text='Приветствую!', reply_markup=keyboard.as_markup())
    
@router.message(F.text)
async def text_working(m: Message):
    keyboard = get_start_keyboard()
    await m.answer(text='Текст я конечно принимаю, но понять его не смогу. Запустите бота', reply_markup=keyboard.as_markup())
    
@router.message(F.sticker)
async def text_working(m: Message):
    keyboard = get_start_keyboard()
    await m.answer(text='Стикеры люблю, но прислать что-то не смогу', reply_markup=keyboard.as_markup())

@router.message(F.photo)
async def text_working(m: Message):
    keyboard = get_start_keyboard()
    await m.answer(text='Я не умею считывать изображения, но Вы можете хранить здесь ещё и фотографии', reply_markup=keyboard.as_markup())
