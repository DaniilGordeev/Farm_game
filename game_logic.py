from datetime import datetime, timedelta, time
import random
from database import Database 

from config import TYPE_BOX

def end_time(growth_hours = 0, growth_minutes = 0):
    planted_at = datetime.now()
    ready_at = planted_at + timedelta(hours=growth_hours, minutes=growth_minutes)
    return ready_at.strftime("%Y-%m-%d %H:%M:%S")

def calculate_end_time(time):
    if isinstance(time, str):
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        
    current_time = datetime.now()
    remaining = time - current_time
        
    # Если время уже прошло
    if remaining <= timedelta(0):
        return True
        
    # Преобразуем timedelta в ЧЧ:ММ:СС
    total_seconds = int(remaining.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
        
    return [f"{hours:02d}:{minutes:02d}:{seconds:02d}", 'replace_time_left', [hours, minutes]]

def random_chance():
    return random.choice([True, False])

def random_chance_resistance(chance):
    number = random.randint(0, 100)
    if number <= chance:
        return True
    else:
        return False
    
def calculate_precent_water(time, full_time):
    if isinstance(time, str):
        time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    if isinstance(time, (int, float)):
        time = datetime.fromtimestamp(time)
        
    current_time = datetime.now()
    remaining = time - current_time
    total_seconds = int(remaining.total_seconds())
    minutes = divmod(total_seconds, 60)[0]
    
    # Если время уже прошло
    if remaining <= timedelta(0):
        return 0
    
    full_time = full_time*60

    return round((minutes/full_time)*100)

def has_time_passed(time_str):
    input_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    current_time = datetime.now()
    return input_time > current_time

def compare_times(time_watering, time_seed):
    # Преобразуем строки в объекты datetime

    if time_watering == '0':
        return True

    time_watering = datetime.strptime(time_watering, '%Y-%m-%d %H:%M:%S')
    time_seed = datetime.strptime(time_seed, '%Y-%m-%d %H:%M:%S')
        
    if time_watering < time_seed:
        return True

def random_resource():
    if random.randint(0, 100) <= 5:
        return random.choice([13, 14, 15, 22])
    

def generate_tasks(user_data, user_money = 499):
    TASK = [
        'Собрать {plant} в количестве {count} шт',
        'Заработать {count} монет'
    ]
    PLANTS = ["Пшеница", "Кукуруза", "Морковь", "Картофель", "Лунный лотос", "Огненный перец"]
    holes = 0
    for i in user_data:
        holes += i['holes']

    tasks = []

    while len(tasks) < 2:
        task = random.choice(TASK)
        db = Database()
        if task == 'Заработать {count} монет':
            count = random.randint(holes*250, holes*400)
            text = task.format(count=count)
            tasks.append({
                'text': text,
                'plant': 0,
                'required': count
            })

        else:
            plant = random.choice(PLANTS)
            id_plant = db.get_items_name(f'{plant} (урожай)')['item_id']

            if plant in ['Лунный лотос', 'Огненный перец']:
                if user_money < 500:
                    continue

            if plant in ['Лунный лотос', 'Огненный перец']:
                count = random.randint(1, round(holes*1.5))
            else:
                count = random.randint(holes, holes*2)

            text = task.format(plant=plant, count=count)
            tasks.append({
                'text': text,
                'plant': id_plant,
                'required': count,
            })
    return tasks



def random_reward_tasks():
    number = random.randint(0, 100)
    money = random.randrange(100, 5100, 100)

    if number >= 0 and number <= 5:
        return [26, money]
    elif number >= 6 and number <= 20:
        return [25, money]
    elif number >= 21 and number <= 40:
        return [24, money]
    else:
        return [23, money]
    

def open_box(box_type):
    if box_type not in TYPE_BOX:
        return None
    
    items = TYPE_BOX[box_type]
    weights = [item[2] for item in items.values()]
    chosen_item = random.choices(list(items.keys()), weights=weights, k=1)[0]
    
    min_q, max_q, _, id = items[chosen_item]
    quantity = random.randint(min_q, max_q)
    
    return {"item": chosen_item, "quantity": quantity, 'id':id}

def is_night_time(current_time=None):
    """
    Проверяет, находится ли текущее время в ночном интервале (22:00 - 8:00)
    
    :param current_time: Время для проверки (datetime.time или None для текущего времени)
    :return: bool - True если ночное время, False если дневное
    """
    if current_time is None:
        current_time = datetime.now().time()
    

    night_start = time(22, 0)  # 22:00
    night_end = time(8, 0)     # 8:00 следующего дня
    
    # Проверяем два возможных случая:
    # 1. Текущее время между 22:00 и 23:59
    # 2. Текущее время между 00:00 и 8:00
    return (current_time >= night_start) or (current_time <= night_end)


def roulette_random():
    number = random.randint(0, 36)
    return number

def dice_random():
    # Диллер
    dice_1_diller = random.randint(1,6)
    dice_2_diller = random.randint(1,6)
    dice_1_user = random.randint(1,6)
    dice_2_user = random.randint(1,6)

    return [[dice_1_diller, dice_2_diller], [dice_1_user, dice_2_user]]

def check_time(end_time):
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()

    if now >= end_time:
        return True
    
    return False

def generate_random_daily_bonus():
    rewards = ['Деньги', 'Бокс', 'Семена']
    reward = random.choice(rewards)

    if reward == 'Деньги':
        quantity = random.randrange(100, 600, 100)
        return [0, quantity] # ID | quantity
    
    if reward == 'Бокс':
        number = random.randint(0, 100)
        if number >= 0 and number <= 5:
            return [26, 1]
        elif number >= 6 and number <= 20:
            return [25, 1]
        elif number >= 21 and number <= 40:
            return [24, 1]
        else:
            return [23, 1]
        
    if reward == 'Семена':
        number = random.randint(0, 100)
        quantity = random.randint(3, 7)
        if 0 <= number <= 2:
            return [5, quantity]
        elif 3 <= number <= 9:
            return [6, quantity]
        elif 10 <= number <= 24:
            return [4, quantity]
        elif 35 <= number <= 54:
            return [3, quantity]
        elif 55 <= number <= 74:
            return [2, quantity]
        else:
            return [1, quantity]
