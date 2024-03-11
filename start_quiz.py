from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, FSInputFile, URLInputFile
import json

router = Router()
def working_with_file(direction: str) -> None:
    with open(direction, 'r', encoding='utf-8', errors='ignore') as file:
        data = json.load(file)
    return data
    
def add_person(id: int, name: str) -> None:
    try:
        data = working_with_file('./info/persons.json')
    except:
        data = {}
    if not str(id) in data:
        data[str(id)] = {"name": name, 'question': 1, 'correct': 0, 'result': 0}
    else:
        data[str(id)] = {"name": name, 'question': 1, 'correct': 0, 'result': 0}
    with open('./info/persons.json', 'w', encoding='utf-8') as file:  
        json.dump(data, file, ensure_ascii=False, indent=4)

def change_result(id: int, callback_data: str) -> str:
    print(callback_data)
    info_about_person = working_with_file('./info/persons.json')
    
    answer = str()
    if callback_data == "start_quiz":
        answer = working_with_file('./info/questions.json')['states'][0]['questions']['1']
        info_about_person[str(id)]['question'] += 1
    else:
        if callback_data == 'start_plus':
            info_about_person[str(id)]['question'] += 1
            info_about_person[str(id)]['correct'] += 1
        else:
            info_about_person[str(id)]['question'] += 1
        if info_about_person[str(id)]['question'] == 5:
            info_about_person[str(id)]['question'] = 1
            result = info_about_person[str(id)]['correct']
            info_about_person[str(id)]['result'] = result
            text = f'Поздравляю с прохождением теста! \n Ваш результат:{info_about_person[str(id)]['result']}/4 \n Спасибо за прохождение\n\n Для повторного прохождения, напишите /start'
            with open('./info/persons.json', 'w', encoding='utf-8') as file:  
                json.dump(info_about_person, file, ensure_ascii=False, indent=4)
            return text
        else:
            answer = working_with_file('./info/questions.json')['states'][0]['questions'][str(info_about_person[str(id)]['question'])]
        with open('./info/persons.json', 'w', encoding='utf-8') as file:  
            json.dump(info_about_person, file, ensure_ascii=False, indent=4)
    return answer
        
def generate_keyboards(id: str) -> InlineKeyboardBuilder:
    info_about_person = working_with_file('./info/persons.json')
    info_about_question= working_with_file('./info/questions.json')
    
    id_quest = str(info_about_person[str(id)]['question'])
    
    keyboard = InlineKeyboardBuilder()
    if info_about_person[str(id)]['result'] == 0:
        for variables in info_about_question['states'][0]['variables'][id_quest]:
            keyboard.add(types.InlineKeyboardButton(text=variables, callback_data=f'{"start_plus" if variables == info_about_question["states"][0]["correct_answers"][id_quest] else "start_false"}'))
    else:
        keyboard.add(types.InlineKeyboardButton(text="Начать по новой", callback_data='start_quiz'))
        keyboard.add(types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data='come_back'))
    keyboard.adjust(1)
    return keyboard

@router.callback_query(lambda F: F.data in ["start_quiz"])
async def start_quiz(callback: CallbackQuery):
    print(callback.from_user.full_name)
    add_person(str(callback.from_user.id), callback.from_user.full_name)
    await callback.message.answer(text='Кем был муж погибший муж Настасьи, Степан?', reply_markup=generate_keyboards(str(callback.from_user.id)).as_markup())
    
@router.callback_query(lambda F: F.data in ["start_plus", "start_false"])
async def quiz_static(callback: CallbackQuery):
    print('ДА МЫ ЗДЕСЬ!', callback.data)
    text = change_result(callback.from_user.id, callback.data)
    await callback.message.answer(text=text, reply_markup=generate_keyboards(str(callback.from_user.id)).as_markup())