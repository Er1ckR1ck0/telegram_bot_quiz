from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
import json

class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def working_with_file(self, direction: str) -> None:
        with open(direction, 'r', encoding='utf-8', errors='ignore') as file:
            data = json.load(file)
        return data   

    def add_person(self, id: int, name: str) -> None:
        try:
            data = self.working_with_file('./info/persons.json')
        except:
            data = {}
        if not str(self.id) in data:
            data[str(self.id)] = {"name": name, 'question': 1, 'correct': 0, 'wrong': 0, 'result': 0}
        else:
            if data[str(self.id)]['question'] < 4:
                pass
            else: 
                data[str(self.id)]['question'] = 1
                data[str(self.id)]['correct'] = 0
                data[str(self.id)]['wrong'] = 0
        with open('./info/persons.json', 'w', encoding='utf-8') as file:  
            json.dump(data, file, ensure_ascii=False, indent=4)

    def change_result(self, id: int, callback_data: str) -> str:
        info_about_person = self.working_with_file('./info/persons.json')
        id_quest = str(info_about_person[str(id)]['question'])
        if callback_data == "start_quiz":
            answer = self.working_with_file('./info/questions.json')['states'][0]['questions'][0]
        else:
            if info_about_person[str(id)]['question'] <= 4: 
                info_about_person[str(id)]['question'] += 1
            else: 
                info_about_person[str(id)]['question'] = 0
                self.result = info_about_person[str(id)]['correct']
                info_about_person[str(id)]['result'] = self.result
                text = f'Поздравляю с прохождением теста! \n Ваш результат:{info_about_person[str(id)]['result']}/{info_about_person[str(id)]['question']} \n Спасибо за прохождение\n\n Для повторного прохождения, напишите /start'
                return text
            if callback_data == 'start_plus':
                answer = self.working_with_file('./info/questions.json')['states'][0]['questions'][id_quest]
                info_about_person[str(id)]['correct'] += 1
                
            else:
                answer = self.working_with_file('./info/questions.json')['states'][0]['questions'][id_quest]
                info_about_person[str(id)]['wrong'] += 1
            

            with open('./info/persons.json', 'w', encoding='utf-8') as file:  
                json.dump(info_about_person, file, ensure_ascii=False, indent=4)
        return answer
            
    def generate_keyboards(self, id: str) -> InlineKeyboardBuilder:
        info_about_person = self.working_with_file('./info/persons.json')
        info_about_question= self.working_with_file('./info/questions.json')
        
        id_quest = str(info_about_person[str(id)]['question'])
        
        keyboard = InlineKeyboardBuilder()
        if info_about_person[str(id)]['question'] <= len(info_about_question['states'][0]['questions']):
            for variables in info_about_question['states'][0]['variables'][id_quest]:
                print(variables, f'{"start_plus" if variables == info_about_question["states"][0]["correct_answers"][id_quest] else "start_false"}')
                keyboard.add(types.InlineKeyboardButton(text=variables, callback_data=f'{"start_plus" if variables == info_about_question["states"][0]["correct_answers"][id_quest] else "start_false"}'))
        else:
            keyboard.add(types.InlineKeyboardButton(text="Начать по новой", callback_data='start_again'))
            keyboard.add(types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data='come_back'))
        keyboard.adjust(1)
        return keyboard

    def get_info(self):
        return self.id, self.name, self.questions, self.correct, self.wrong
    
    def start_again(self):
        info_about_person = self.working_with_file('./info/persons.json')
        info_about_person[str(self.id)] = {"name": self.name, 'question': 1, 'correct': 0, 'wrong': 0, 'result': 0}