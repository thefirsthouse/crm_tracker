import json
import os
from typing import Union

class Unit:
    @staticmethod
    def _get_next_id(filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as datafile:
                try:
                    existing_data = json.load(datafile)
                    return len(existing_data) + 1  # ID = количество записей + 1
                except json.JSONDecodeError:
                    return 1  # Если файл пустой или повреждён
        else:
            return 1  # Если файл отсутствует

    def __init__(self, name: str, group: str, last_contact: str):
        # Генерация уникального ID
        filepath = 'database/data.json'
        self.id = Unit._get_next_id(filepath)
        self.name = name
        self.group = group
        self.last_contact = last_contact

        # Данные объекта
        self.data = {
            'id': self.id,
            'name': self.name,
            'group': self.group,
            'last_contact': self.last_contact
        }

    def add(self):
        # Создаём папку, если она отсутствует
        os.makedirs('database', exist_ok=True)
        filepath = 'database/data.json'

        # Читаем существующие данные
        if os.path.exists(filepath):
            with open(filepath, 'r') as datafile:
                try:
                    existing_data = json.load(datafile)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        # Добавляем текущий объект
        existing_data.append(self.data)

        # Перезаписываем файл
        with open(filepath, 'w') as datafile:
            json.dump(existing_data, datafile, indent=4)


def show_all() -> None:
    filepath = 'database/data.json'
    try:
        with open(filepath, 'r') as datafile:
            data = json.load(datafile)
            if data:
                for item in data:
                    print(item['id'], '|', item['name'], '|', item['group'], '|', item['last_contact'])
            else:
                print('You have no units.')
    except FileNotFoundError:
        with open(filepath, 'a') as datafile:
            print('You have no units.')
    except json.JSONDecodeError:
        print('Database file is corrupted.')


# def show_unit(id) -> Union[dict, str]:
#     output = None
#     filepath = 'database/data.json'
#     with open(filepath, 'r') as datafile:
#         data = json.load(datafile)
#         if data:
#             for item in data:
#                 if item['id'] == id + 1:
#                     output = item
#                     break
#             else:
#                 output = ('There is no units with this number')
#     return output


if __name__ == '__main__':
    show_all()

    action = (input('Add new? (y/n): '))
    match action:
        case 'y':
            try:
                name = str(input('Name: '))
                group = str(input('Group: '))
                last_contact = str(input('Last contact: '))
            finally:
                new = Unit(name, group, last_contact)
                new.add()
            show_all()
        case 'n':
            pass
