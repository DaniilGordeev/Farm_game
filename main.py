import telebot
import schedule
import threading
import time


from config import TOKEN, HARVEST, PRICE_UPGRADE_DISEASE_RESISTANCE, PRICE_UPGRADE_TIME_WATERING, \
                    PRICE_BUY_BEDS, ID_CHANNEL_MARKET, ID_CHANNEL_NEWS, ID_ITEM_FOR_SELL, ID_CHAT_REPORTS
from database import Database
import keyboard as kb
import game_logic as gl
import create_table
TOKEN = "8055869737:AAEsL52Eh_jEsOSHbzQ3RjWNAJByfgY_Gd0"
bot = telebot.TeleBot(TOKEN)

create_table.create_database()
create_table.update_database_schema()

@bot.callback_query_handler(lambda call: call.data == 'continue_training')
def continue_training(call):
    id = call.from_user.id
    bot.delete_messages(id, [call.message.message_id, call.message.message_id-1])

@bot.message_handler(commands=['start'])
def start(message):
    id = message.from_user.id
    db = Database()
    if db.check_users(id) == True: # Проверка на существование пользователя в БД
        db.set_user(id, gl.end_time(4))
        db.set_farm(id)
        db.set_bed(id, 1, gl.end_time(8))
        db.set_inventory(id, 1, 10)
        info_of_user = db.get_info_for_tasks(id)
        db.set_tasks(id, gl.generate_tasks(info_of_user, user['money']))
        text = f'🌻 Привет, будущий фермер! 🌻\n'\
                f'Перед тобой бескрайние поля, где:\n'\
                f'• Каждое семя — начало новой истории\n'\
                f'• Каждый урожай — маленькое достижение\n'\
                f'• Каждый день приносит что-то новое\n'\
                f'Ферма ждет твоего прикосновения.\n\n'\
                f"👣 Давай пройдем небольшое обучение, оно не займет много времени!"
        bot.send_message(id, text, reply_markup=kb.start_kb)
    else:
        user = db.get_me(id)
        if user['locate'] == 'training':
            bot.send_message(id, 
                         "⛔ Пожалуйста, используйте кнопки для прохождения обучения. Вы не можете использовать другие команды сейчас.", 
                         reply_markup=kb.continue_training_kb)
            return

        if gl.has_time_passed(user['buster_x10_time_all']) == False:
            text = f'🌟 Профиль 🌟\n'\
                    f'══════════════\n'\
                    f'🆔 Твой ID: {id}\n'\
                    f'💰 Монет: {user["money"]}\n'\
                    f'🪙 Золотых монет: {user["gold_money"]}\n'\
                    f'══════════════'
        else:
            text = f'🌟 Профиль 🌟\n'\
                    f'══════════════\n'\
                    f'🆔 Твой ID: {id}\n'\
                    f'💰 Монет: {user["money"]}\n'\
                    f'🪙 Золотых монет: {user["gold_money"]}\n'\
                    f'⚡У тебя активирован бустер:\n'\
                    f'⏳⚡Быстрее в 10 раз\n'\
                    f'══════════════'
        bot.send_message(id, text, reply_markup=kb.profile_kb)
    db.edit_locate(id, 'start')

# Обучение

@bot.callback_query_handler(lambda call: call.data == 'pass_training')
def pass_training(call):
    id = call.from_user.id
    db = Database()
    db.edit_locate(id, 'training')
    text = "🌾 *Добро пожаловать на ферму!* 🌾\n\n"\
           "Давай начнём с осмотра твоих владений."
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.farm_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'bed_training')
def bed_training(call):
    id = call.from_user.id
    text =  "🪱 *[ Твоя первая грядка ]* 🪱\n\n"\
            "▸ 🎯 *Доступно лунок:* 5\n"\
            "▸ 🛠️ *Грабли:* ❌\n"\
            "▸ 🌱 *Состояние:* Пусто\n"\
            "▸ 💧 *Влажность почвы:* 100%\n\n"\
            "*Как это работает:*\n"\
            "1️⃣ Нужно посадить семена\n"\
            "2️⃣ Для сбора урожая потребуются грабли\n"\
            "3️⃣ Всё необходимое найдёшь в магазине\n\n"\
            "Давай отправимся за покупками!"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.in_shop_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'in_shop')
def in_shop(call):
    id = call.from_user.id
    text = "🏪 *Магазин фермера*\n\n"\
           "Здесь ты можешь приобрести всё необходимое для работы.\n"\
           "Давай начнём с выбора семян!"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.seeds_training_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'seed')
def seed(call):
    id = call.from_user.id
    text = "🌾 *Отдел семян*\n\n"\
           "Остался последний пакет пшеницы!\n"\
           "Отличный выбор для начала - пшеница неприхотлива и быстро растёт."
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.buy_wheat_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'buy_wheat_training')
def buy_wheat_training(call):
    id = call.from_user.id
    text = "📦 *Пшеничные семена*\n\n"\
           "В наличии как раз 5 пакетиков - идеально для твоей грядки!\n"\
           "Хватай пока не разобрали!"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.buy_wheat_5_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'buy_wheat_5')
def buy_wheat_5(call):
    id = call.from_user.id
    text = "✅ *Отличная покупка!*\n\n"\
           "Семена пшеницы теперь в твоём инвентаре!\n\n"\
           "Теперь нужно приобрести грабли - без них урожай не собрать."
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.rake_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'rake_training')
def rake_training(call):
    id = call.from_user.id
    text = "🛠️ *Отдел инвентаря*\n\n"\
           "Для начала подойдут простые *деревянные грабли*.\n"\
           "Позже ты сможешь приобрести более профессиональные инструменты."
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.buy_rake_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'buy_rake_training')
def buy_rake_training(call):
    id = call.from_user.id
    text = "🎉 *Базовый набор готов!*\n\n"\
           "Теперь у тебя есть всё необходимое:\n"\
           "▸ Семена пшеницы\n"\
           "▸ Деревянные грабли\n\n"\
           "Возвращаемся на ферму - время поработать!"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.farm_work_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'farm_work')
def farm_work(call):
    id = call.from_user.id
    text =  "🪱 *[ Твоя грядка ]* 🪱\n\n"\
            "▸ 🎯 *Лунок:* 5\n"\
            "▸ 🛠️ *Грабли:* Деревянные ✅\n"\
            "▸ 🌱 *Состояние:* Пусто\n"\
            "▸ 💧 *Влажность:* 100%\n\n"\
            "Пора посадить наши семена пшеницы!"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.set_seed_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'set_seed_training')
def set_seed_training(call):
    id = call.from_user.id
    text = "🌱 *Посадка завершена!*\n\n"\
           "Семена пшеницы успешно высажены!\n\n"\
           "Для обучения ускорю процесс - урожай уже готов к сбору!"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.get_harvest_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'get_harvest_training')
def get_harvest_training(call):
    id = call.from_user.id
    text = "🎉 *Первый урожай!*\n\n"\
           "Ты получил:\n"\
           "▸ 5 единиц пшеницы\n"\
           "▸ Редкий ресурс: *Молекула дождя* 🌧️\n\n"\
           "*Интересный факт:*\n"\
           "Редкие ресурсы используются для покупки эксклюзивного инвентаря!\n\n"\
           "Теперь покажу, как продавать урожай."
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.go_buyer_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'go_buyer')
def go_buyer(call):
    id = call.from_user.id
    text = "👨‍🌾 *Местный скупщик*\n\n"\
           "Здесь ты можешь быстро продать свой урожай за монеты.\n"\
           "Не самый выгодный, но самый простой способ заработка."
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.sell_harvest_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'sell_harvest_training')
def sell_harvest_training(call):
    id = call.from_user.id
    text = "💰 *Продажа завершена!*\n\n"\
           "Ты получил свои первые монеты!\n\n"\
           "Но это не единственный способ заработка.\n"\
           "Покажу более выгодный вариант..."
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.go_market_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'go_market')
def go_market(call):
    id = call.from_user.id
    text = "🏪 *Фермерский рынок*\n\n"\
           "@farmhappymarket\n\n"\
           "Здесь ты можешь:\n"\
           "▸ Продавать товары другим игрокам\n"\
           "▸ Покупать товары по выгодным ценам\n"\
           "▸ Находить редкие ресурсы\n\n"\
           "Отличное место для выгодных сделок!"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.end_training_kb, parse_mode='Markdown')

@bot.callback_query_handler(lambda call: call.data == 'end_training')
def end_training(call):
    id = call.from_user.id
    text = "🎓 *Обучение завершено!*\n\n"\
           "Теперь ты знаешь основы фермерства:\n"\
           "▸ Как выращивать урожай\n"\
           "▸ Как продавать товары\n"\
           "▸ Где искать лучшие сделки\n\n"\
           "Желаю обильных урожаев и больших прибылей!\n"\
           "Вперёд к новым достижениям! 🌟"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.go_game_kb, parse_mode='Markdown')



@bot.message_handler(commands=['profile'])
def profile(message):
    id = message.from_user.id
    db = Database()
    user = db.get_me(id)

    if user['locate'] == 'training':
        bot.send_message(id, 
                         "⛔ Пожалуйста, используйте кнопки для прохождения обучения. Вы не можете использовать другие команды сейчас.", 
                         reply_markup=kb.continue_training_kb)
        return
    
    if gl.has_time_passed(user['buster_x10_time_all']) == False:
        text = f'🌟 Профиль 🌟\n'\
                f'══════════════\n'\
                f'🆔 Твой ID: {id}\n'\
                f'💰 Монет: {user["money"]}\n'\
                f'🪙 Золотых монет: {user["gold_money"]}\n'\
                f'══════════════'
    else:
        text = f'🌟 Профиль 🌟\n'\
                f'══════════════\n'\
                f'🆔 Твой ID: {id}\n'\
                f'💰 Монет: {user["money"]}\n'\
                f'🪙 Золотых монет: {user["gold_money"]}\n'\
                f'⚡У тебя активирован бустер:\n'\
                f'⏳⚡Быстрее в 10 раз\n'\
                f'══════════════'
    bot.send_message(id, text, reply_markup=kb.profile_kb)

@bot.callback_query_handler(lambda call: call.data == 'profile')
def profile(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    if gl.has_time_passed(user['buster_x10_time_all']) == False:
        text = f'🌟 Профиль 🌟\n'\
                f'══════════════\n'\
                f'🆔 Твой ID: {id}\n'\
                f'💰 Монет: {user["money"]}\n'\
                f'🪙 Золотых монет: {user["gold_money"]}\n'\
                f'══════════════'
    else:
        text = f'🌟 Профиль 🌟\n'\
                f'══════════════\n'\
                f'🆔 Твой ID: {id}\n'\
                f'💰 Монет: {user["money"]}\n'\
                f'🪙 Золотых монет: {user["gold_money"]}\n'\
                f'⚡У тебя активирован бустер:\n'\
                f'⏳⚡Быстрее в 10 раз\n'\
                f'══════════════'
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.profile_kb)
    db.edit_locate(id, 'profile')

@bot.callback_query_handler(lambda call: call.data == 'clans')
def clans(call):
    id = call.from_user.id 
    text = f'Скоро...'
    bot.answer_callback_query(call.id, text)

@bot.callback_query_handler(lambda call: call.data == 'tasks')
def tasks(call):
    id = call.from_user.id 
    db = Database()
    tasks = db.get_tasks(id)
    if tasks['task1_completed'] != -1 and tasks['task2_completed'] != -1:
        text = f'📅 **Задания на сегодня** 📅\n\n'\
                f'✅ **Задание 1**\n'\
                f'➖ {tasks["text_task1"]}\n'\
                f'✔ Выполнено {tasks["task1_completed"]}\n\n'\
                f'✅ **Задание 2**\n'\
                f'➖ {tasks["text_task2"]}\n'\
                f'✔ Выполнено {tasks["task2_completed"]}'
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_profile_kb)
    
    if tasks['task1_completed'] == -1 and tasks['task2_completed'] == -1:
        if tasks['get_reward'] == 0:
            text = f'📅 **Задания на сегодня** 📅\n\n'\
                    f'✅ **Задание 1**\n'\
                    f'➖ {tasks["text_task1"]}\n'\
                    f'✔ Выполнено: Готово\n\n'\
                    f'✅ **Задание 2**\n'\
                    f'➖ {tasks["text_task2"]}\n'\
                    f'✔ Выполнено: Готово\n'\
                    f'✅Можешь забрать награду'
            bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.get_reward_kb)
        else:
            text = f'📅 **Задания на сегодня** 📅\n\n'\
                    f'✅ **Задание 1**\n'\
                    f'➖ {tasks["text_task1"]}\n'\
                    f'✔ Выполнено: Готово\n\n'\
                    f'✅ **Задание 2**\n'\
                    f'➖ {tasks["text_task2"]}\n'\
                    f'✔ Выполнено: Готово'
            bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_profile_kb)

    if tasks['task1_completed'] == -1 and tasks['task2_completed'] != -1:
        text = f'📅 **Задания на сегодня** 📅\n\n'\
                f'✅ **Задание 1**\n'\
                f'➖ {tasks["text_task1"]}\n'\
                f'✔ Выполнено: Готово\n\n'\
                f'✅ **Задание 2**\n'\
                f'➖ {tasks["text_task2"]}\n'\
                f'✔ Выполнено {tasks["task2_completed"]}'
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_profile_kb)
        
    if tasks['task1_completed'] != -1 and tasks['task2_completed'] == -1:
        text = f'📅 **Задания на сегодня** 📅\n\n'\
                f'✅ **Задание 1**\n'\
                f'➖ {tasks["text_task1"]}\n'\
                f'✔ Выполнено {tasks["task1_completed"]}\n\n'\
                f'✅ **Задание 2**\n'\
                f'➖ {tasks["text_task2"]}\n'\
                f'✔ Выполнено: Готово'
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_profile_kb)

@bot.callback_query_handler(lambda call: call.data == 'get_reward')
def get_reward(call):
    id = call.from_user.id 
    db = Database()
    reward = gl.random_reward_tasks()
    box = db.get_items_id(reward[0])
    text = f'✨ ━━━━━━━━━━━ ✨\n'\
            f'  🎁 **{box["name"]}**\n'\
            f'✨ ━━━━━━━━━━━ ✨\n\n'\
            f'🪙 **+{reward[1]} монет** 🪙'
    db.set_inventory(id, reward[0], 1)
    db.add_money(id, reward[1])
    db.edit_get_reward(id)
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_tasks_kb)

@bot.message_handler(commands=['inventory'])
def inventory(message):
    id = message.from_user.id
    db = Database()
    user = db.get_me(id)

    if user['locate'] == 'training':
        bot.send_message(id, 
                         "⛔ Пожалуйста, используйте кнопки для прохождения обучения. Вы не можете использовать другие команды сейчас.", 
                         reply_markup=kb.continue_training_kb)
        return
    
    items = db.get_inventory(id)
    text = '🧰 Инвентарь\n\n'
    if not items:
        text = f'Твой инветарь пуст!'
    
    for item in items:
        text += f"🆔 {item['item_id']} │ {item['name']} │ x{item['quantity']} │\n"
    bot.send_message(id, text, reply_markup=kb.box_kb)

@bot.callback_query_handler(lambda call: call.data == 'inventory')
def inventory(call):
    id = call.from_user.id
    db = Database()
    items = db.get_inventory(id)
    text = ''
    if not items:
        text = f'Твой инветарь пуст!'
    
    for item in items:
        text += f"│ {item['name']} │ x{item['quantity']} │\n"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.box_kb)

@bot.message_handler(commands=['city'])
def city(message):
    id = message.from_user.id 
    db = Database()
    user = db.get_me(id)

    if user['locate'] == 'training':
        bot.send_message(id, 
                         "⛔ Пожалуйста, используйте кнопки для прохождения обучения. Вы не можете использовать другие команды сейчас.", 
                         reply_markup=kb.continue_training_kb)
        return
    
    text = f"➡️ Выбери направление:"
    bot.send_message(id, text, reply_markup=kb.city_kb)

@bot.callback_query_handler(lambda call: call.data == 'city')
def city_call(call):
    id = call.from_user.id 
    text = f"➡️ Выбери направление:"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.city_kb)


@bot.callback_query_handler(lambda call: call.data == 'buyer')
def buyer(call):
    id = call.from_user.id 
    db = Database()
    inventory_user = db.get_item_inventory_type(id, 'урожай')
    text = f"🌱 *Фермерский рынок* 🏪\n\n"\
            f"📃 Прайс-лист Скупщика:\n"\
            f"<i>🔹 Пшеница — 15 монет</i>\n"\
            f"<i>🔹 Морковь — 30 монет</i>\n"\
            f"<i>🔹 Кукуруза — 40 монет</i>\n"\
            f"<i>🔹 Картофель — 80 монет</i>\n"\
            f"<i>🔹 Лунный лотос — 800 монет</i>\n"\
            f"<i>🔹 Огненный перец — 450 монет</i>"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.buyer(inventory_user), parse_mode='html')
    
@bot.callback_query_handler(lambda call: call.data == 'sell_item_16')
def sell_item_16(call):
    id = call.from_user.id 
    db = Database()
    item = db.get_item_invetory(id, 16)
    price = db.get_items_id(16)['sell_price']
    tasks = db.get_tasks(id)
    summa = price*item['quantity']
    text = f"💰 *Удачная сделка!* 💰\nТы продал весь урожай пшеницы за {summa} монет!"
    db.add_money(id, summa)
    db.remove_item_id(id, 16, item['quantity'])

    if tasks['plant1'] == 0 and tasks['task1_completed'] != -1:
        db.update_completed_task(id, 1, summa)
    if tasks['plant2'] == 0 and tasks['task2_completed'] != -1:
        db.update_completed_task(id, 2, summa)

    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_buyer_kb)

@bot.callback_query_handler(lambda call: call.data == 'sell_item_17')
def sell_item_17(call):
    id = call.from_user.id 
    db = Database()
    item = db.get_item_invetory(id, 17)
    price = db.get_items_id(17)['sell_price']
    tasks = db.get_tasks(id)
    summa = price*item['quantity']
    text = f"💰 *Удачная сделка!* 💰\nТы продал весь урожай моркови за {summa} монет!"
    db.add_money(id, summa)
    db.remove_item_id(id, 17, item['quantity'])

    if tasks['plant1'] == 0 and tasks['task1_completed'] != -1:
        db.update_completed_task(id, 1, summa)
    if tasks['plant2'] == 0 and tasks['task2_completed'] != -1:
        db.update_completed_task(id, 2, summa)

    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_buyer_kb)

@bot.callback_query_handler(lambda call: call.data == 'sell_item_18')
def sell_item_18(call):
    id = call.from_user.id 
    db = Database()
    item = db.get_item_invetory(id, 18)
    price = db.get_items_id(18)['sell_price']
    tasks = db.get_tasks(id)
    summa = price*item['quantity']
    text = f"💰 *Удачная сделка!* 💰\nТы продал весь урожай кукурузы за {summa} монет!"
    db.add_money(id, summa)
    db.remove_item_id(id, 18, item['quantity'])

    if tasks['plant1'] == 0 and tasks['task1_completed'] != -1:
        db.update_completed_task(id, 1, summa)
    if tasks['plant2'] == 0 and tasks['task2_completed'] != -1:
        db.update_completed_task(id, 2, summa)

    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_buyer_kb)

@bot.callback_query_handler(lambda call: call.data == 'sell_item_19')
def sell_item_19(call):
    id = call.from_user.id 
    db = Database()
    item = db.get_item_invetory(id, 19)
    price = db.get_items_id(19)['sell_price']
    tasks = db.get_tasks(id)
    summa = price*item['quantity']
    text = f"💰 *Удачная сделка!* 💰\nТы продал весь урожай картофеля за {summa} монет!"
    db.add_money(id, summa)
    db.remove_item_id(id, 19, item['quantity'])

    if tasks['plant1'] == 0 and tasks['task1_completed'] != -1:
        db.update_completed_task(id, 1, summa)
    if tasks['plant2'] == 0 and tasks['task2_completed'] != -1:
        db.update_completed_task(id, 2, summa)

    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_buyer_kb)

@bot.callback_query_handler(lambda call: call.data == 'sell_item_20')
def sell_item_20(call):
    id = call.from_user.id 
    db = Database()
    item = db.get_item_invetory(id, 20)
    price = db.get_items_id(20)['sell_price']
    tasks = db.get_tasks(id)
    summa = price*item['quantity']
    text = f"💰 *Удачная сделка!* 💰\nТы продал весь урожай лунного лотоса за {summa} монет!"
    db.add_money(id, summa)
    db.remove_item_id(id, 20, item['quantity'])

    if tasks['plant1'] == 0 and tasks['task1_completed'] != -1:
        db.update_completed_task(id, 1, summa)
    if tasks['plant2'] == 0 and tasks['task2_completed'] != -1:
        db.update_completed_task(id, 2, summa)

    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_buyer_kb)

@bot.callback_query_handler(lambda call: call.data == 'sell_item_21')
def sell_item_21(call):
    id = call.from_user.id 
    db = Database()
    item = db.get_item_invetory(id, 21)
    price = db.get_items_id(21)['sell_price']
    tasks = db.get_tasks(id)
    summa = price*item['quantity']
    text = f"💰 *Удачная сделка!* 💰\nТы продал весь урожай огненного перца за {summa} монет!"
    db.add_money(id, summa)
    db.remove_item_id(id, 21, item['quantity'])

    if tasks['plant1'] == 0 and tasks['task1_completed'] != -1:
        db.update_completed_task(id, 1, summa)
    if tasks['plant2'] == 0 and tasks['task2_completed'] != -1:
        db.update_completed_task(id, 2, summa)

    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_buyer_kb)

@bot.callback_query_handler(lambda call: call.data == 'shop')
def shop(call):
    id = call.from_user.id
    text = f"🚜 *Добро пожаловать в Фермерский магазин!* 🌾\n"\
            f"Выбери интересующую категорию товаров:"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.shop_kb)

@bot.callback_query_handler(lambda call: call.data == 'seeds')
def seeds(call):
    id = call.from_user.id
    text = f'Семена\n'
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.seeds_kb)

@bot.callback_query_handler(lambda call: call.data == 'seeds_2')
def seeds_2(call):
    id = call.from_user.id 
    bot.edit_message_reply_markup(id, call.message.message_id, reply_markup=kb.seeds_2_kb)


@bot.callback_query_handler(lambda call: call.data == 'buy_wheat')
def buy_wheat(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    db.edit_locate(id, 'buy_wheat')
    item = db.get_items_id(1)
    text = f"▄▄▄▄▄▄▄▄▄▄▄▄▄\n"\
            f"{item['name']}\n"\
            f"▀▀▀▀▀▀▀▀▀▀▀▀▀\n"\
            f"{item['price']} монет\n"\
            f"🪙 Твои монеты: {user['money']}"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.card_seeds_kb)

@bot.callback_query_handler(lambda call: call.data == 'buy_carrot')
def buy_carrot(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    db.edit_locate(id, 'buy_carrot')
    item = db.get_items_id(2)
    text = f"▄▄▄▄▄▄▄▄▄▄▄▄▄\n"\
            f"{item['name']}\n"\
            f"▀▀▀▀▀▀▀▀▀▀▀▀▀\n"\
            f"{item['price']} монет\n"\
            f"🪙 Твои монеты: {user['money']}"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.card_seeds_kb)

@bot.callback_query_handler(lambda call: call.data == 'buy_corn')
def buy_corn(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    db.edit_locate(id, 'buy_corn')
    item = db.get_items_id(3)
    text = f"▄▄▄▄▄▄▄▄▄▄▄▄▄\n"\
            f"{item['name']}\n"\
            f"▀▀▀▀▀▀▀▀▀▀▀▀▀\n"\
            f"{item['price']} монет\n"\
            f"🪙 Твои монеты: {user['money']}"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.card_seeds_kb)

@bot.callback_query_handler(lambda call: call.data == 'buy_potato')
def buy_potato(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    db.edit_locate(id, 'buy_potato')
    item = db.get_items_id(4)
    text = f"▄▄▄▄▄▄▄▄▄▄▄▄▄\n"\
            f"{item['name']}\n"\
            f"▀▀▀▀▀▀▀▀▀▀▀▀▀\n"\
            f"{item['price']} монет\n"\
            f"🪙 Твои монеты: {user['money']}"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.card_seeds_kb)

@bot.callback_query_handler(lambda call: call.data == 'buy_moon_lotus')
def buy_moon_lotus(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    db.edit_locate(id, 'buy_moon_lotus')
    item = db.get_items_id(5)
    text = f"▄▄▄▄▄▄▄▄▄▄▄▄▄\n"\
            f"{item['name']}\n"\
            f"▀▀▀▀▀▀▀▀▀▀▀▀▀\n"\
            f"{item['price']} монет\n"\
            f"🪙 Твои монеты: {user['money']}"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.card_seeds_kb)

@bot.callback_query_handler(lambda call: call.data == 'buy_fire_pepper')
def buy_fire_pepper(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    db.edit_locate(id, 'buy_fire_pepper')
    item = db.get_items_id(6)
    text = f"▄▄▄▄▄▄▄▄▄▄▄▄▄\n"\
            f"{item['name']}\n"\
            f"▀▀▀▀▀▀▀▀▀▀▀▀▀\n"\
            f"{item['price']} монет\n"\
            f"🪙 Твои монеты: {user['money']}"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.card_seeds_kb)


@bot.callback_query_handler(lambda call: call.data == 'quantity_buy_1')
def quantity_buy_1(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    if user['locate'] == 'buy_wheat':
        item = db.get_items_id(1)
    if user['locate'] == 'buy_corn':
        item = db.get_items_id(3)
    if user['locate'] == 'buy_carrot':
        item = db.get_items_id(2)
    if user['locate'] == 'buy_potato':
        item = db.get_items_id(4)
    if user['locate'] == 'buy_moon_lotus':
        item = db.get_items_id(5)
    if user['locate'] == 'buy_fire_pepper':
        item = db.get_items_id(6)

    if user['money'] >= item['price']:
        db.set_inventory(id, int(item['item_id']))
        db.edit_money(id, int(item['price']))
        user = db.get_me(id)
        text = f"✅ Куплено: **{item['name']}** (1 шт.)"
        text_for_message = f"▄▄▄▄▄▄▄▄▄▄▄▄▄\n"\
            f"{item['name']}\n"\
            f"▀▀▀▀▀▀▀▀▀▀▀▀▀\n"\
            f"{item['price']} монет\n"\
            f"🪙 Твои монеты: {user['money']}"
        bot.edit_message_text(text_for_message, id, call.message.message_id, reply_markup=kb.card_seeds_kb)
    else:
        text = f"😢 Упс! Не хватает монет..."
    bot.answer_callback_query(call.id, text)

@bot.callback_query_handler(lambda call: call.data == 'quantity_buy_5')
def quantity_buy_5(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    if user['locate'] == 'buy_wheat':
        item = db.get_items_id(1)
    if user['locate'] == 'buy_corn':
        item = db.get_items_id(3)
    if user['locate'] == 'buy_carrot':
        item = db.get_items_id(2)
    if user['locate'] == 'buy_potato':
        item = db.get_items_id(4)
    if user['locate'] == 'buy_moon_lotus':
        item = db.get_items_id(5)
    if user['locate'] == 'buy_fire_pepper':
        item = db.get_items_id(6)

    if user['money'] >= item['price']*5:
        db.set_inventory(id, int(item['item_id']), 5)
        db.edit_money(id, int(item['price'])*5)
        user = db.get_me(id)
        text = f"✅ Куплено: **{item['name']}** (5 шт.)"
        text_for_message = f"▄▄▄▄▄▄▄▄▄▄▄▄▄\n"\
            f"{item['name']}\n"\
            f"▀▀▀▀▀▀▀▀▀▀▀▀▀\n"\
            f"{item['price']} монет\n"\
            f"🪙 Твои монеты: {user['money']}"
        bot.edit_message_text(text_for_message, id, call.message.message_id, reply_markup=kb.card_seeds_kb)
    else:
        text = f"😢 Упс! Не хватает монет..."
    bot.answer_callback_query(call.id, text)

@bot.callback_query_handler(lambda call: call.data == 'quantity_buy_10')
def quantity_buy_10(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    if user['locate'] == 'buy_wheat':
        item = db.get_items_id(1)
    if user['locate'] == 'buy_corn':
        item = db.get_items_id(3)
    if user['locate'] == 'buy_carrot':
        item = db.get_items_id(2)
    if user['locate'] == 'buy_potato':
        item = db.get_items_id(4)
    if user['locate'] == 'buy_moon_lotus':
        item = db.get_items_id(5)
    if user['locate'] == 'buy_fire_pepper':
        item = db.get_items_id(6)

    if user['money'] >= item['price']*10:
        db.set_inventory(id, int(item['item_id']), 10)
        db.edit_money(id, int(item['price'])*10)
        user = db.get_me(id)
        text = f"✅ Куплено: **{item['name']}** (10 шт.)"
        text_for_message = f"▄▄▄▄▄▄▄▄▄▄▄▄▄\n"\
            f"{item['name']}\n"\
            f"▀▀▀▀▀▀▀▀▀▀▀▀▀\n"\
            f"{item['price']} монет\n"\
            f"🪙 Твои монеты: {user['money']}"
        bot.edit_message_text(text_for_message, id, call.message.message_id, reply_markup=kb.card_seeds_kb)
    else:
        text = f"😢 Упс! Не хватает монет..."
    bot.answer_callback_query(call.id, text)

@bot.callback_query_handler(lambda call: call.data == 'rakes')
def rakes(call):
    id = call.from_user.id
    text = f'Грабли'
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.rakes_kb)

@bot.callback_query_handler(lambda call: call.data == 'rakes_2')
def rakes_2(call):
    id = call.from_user.id 
    bot.edit_message_reply_markup(id, call.message.message_id, reply_markup=kb.rakes_2_kb)

@bot.callback_query_handler(lambda call: call.data == 'buy_wood_rake')
def buy_wood_rake(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    db.edit_locate(id, 'buy_wood_rake')
    item = db.get_items_id(7)
    text =  f"🪓 ДЕРЕВЯННЫЕ ГРАБЛИ 🪓\n"\
            f"├ 🛡️ Прочность: 20 использований\n"\
            f"└ 💰 Цена: {item['price']} монет\n"\
            f"🪙 Твои монеты: {user['money']}"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.card_rakes_kb)

@bot.callback_query_handler(lambda call: call.data == 'buy_iron_rake')
def buy_iron_rake(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    db.edit_locate(id, 'buy_iron_rake')
    item = db.get_items_id(9)
    text =  f"🔨 ЖЕЛЕЗНЫЕ ГРАБЛИ 🔨\n"\
            f"├ 🚜 Эффект: +2 к урожаю с грядки\n"\
            f"├ 🛡️ Прочность: 30 использований\n"\
            f"└ 💰 Цена: {item['price']} монет\n"\
            f"🪙 Твои монеты: {user['money']}"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.card_rakes_kb)

@bot.callback_query_handler(lambda call: call.data == 'buy_steel_rake')
def buy_steel_rake(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    db.edit_locate(id, 'buy_steel_rake')
    item = db.get_items_id(8)
    text =  f"🔧 СТАЛЬНЫЕ ГРАБЛИ 🔧\n"\
            f"├ 🌟 Эффект: +3🍅 к урожаю с грядки\n"\
            f"├ 🛡️ Прочность: 40 использований\n"\
            f"└ 💰 Цена: {item['price']} монет\n"\
            f"🪙 Твои монеты: {user['money']}"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.card_rakes_kb)

@bot.callback_query_handler(lambda call: call.data == 'buy_rain_rake')
def buy_rain_rake(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    db.edit_locate(id, 'buy_rain_rake')
    item = db.get_items_id(10)
    text =  f"☔ ГРАБЛИ ДОЖДЯ ☔\n"\
            f"├ 🌊 Эффект: 2x влажность грядок\n"\
            f"├ ⚠ Особенность: -1 прочность за полив/сбор\n"\
            f"├ 🛡️ Прочность: 50 использований\n"\
            f"├ 💰 Цена: \n"\
            f"├ 🪙 {item['price']} монет\n"\
            f"└ 💧 5 молекул дождя\n"\
            f"🪙 Твои монеты: {user['money']}"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.card_rakes_kb)

@bot.callback_query_handler(lambda call: call.data == 'buy_dreams_rake')
def buy_dreams_rake(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    db.edit_locate(id, 'buy_dreams_rake')
    item = db.get_items_id(11)
    text =  f"✨ ГРАБЛИ СНОВИДЕНИЙ ✨\n"\
            f"├ 🌙 Эффект: 2x урожай (22:00-8:00 МСК)\n"\
            f"├ 🛡️ Прочность: 50 использований\n"\
            f"├ 💰 Цена: \n"\
            f"├ 🪙 {item['price']} монет\n"\
            f"└ 🌿 5 сновиденческие травы\n"\
            f"🪙 Твои монеты: {user['money']}"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.card_rakes_kb)

@bot.callback_query_handler(lambda call: call.data == 'buy_quantum_rake')
def buy_quantum_rake(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    db.edit_locate(id, 'buy_quantum_rake')
    item = db.get_items_id(12)
    text =  f"🌌 КВАНТОВЫЕ ГРАБЛИ 🌌\n"\
            f"├ ⚡ Эффект: 50% шанс 2x урожая\n"\
            f"├ 🛡️ Прочность: 50 квантовых циклов\n"\
            f"├ 💰 Цена: \n"\
            f"├ 🪙 {item['price']} монет\n"\
            f"└ ⚛️ 5 квантовых обломоков\n"\
            f"🪙 Твои монеты: {user['money']}"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.card_rakes_kb)

@bot.callback_query_handler(lambda call: call.data == 'buy_rakes')
def buy_rakes(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_tool = db.get_rake(id)

    if user['locate'] == 'buy_wood_rake':
        item = db.get_items_id(7)
        resource = [0, 0] # ID ресурса, количество
    if user['locate'] == 'buy_iron_rake':
        item = db.get_items_id(9)
        resource = [0, 0]
    if user['locate'] == 'buy_steel_rake':
        item = db.get_items_id(8)
        resource = [0, 0]
    if user['locate'] == 'buy_rain_rake':
        item = db.get_items_id(10)
        resource = [13, 5]
    if user['locate'] == 'buy_dreams_rake':
        item = db.get_items_id(11)
        resource = [14, 5]
    if user['locate'] == 'buy_quantum_rake':
        item = db.get_items_id(12)
        resource = [15, 5]

    if user['money'] >= item['price']:
        if resource[0] == 13:
            if db.get_item_invetory(id, 13)['quantity'] < 5:
                text = f"❌ Нехватает ресурса для покупки"
                bot.answer_callback_query(call.id, text)
                return
            else:
                db.remove_item_id(id, 13, 5)
        if resource[0] == 14:
            if db.get_item_invetory(id, 14)['quantity'] < 5:
                text = f"❌ Нехватает ресурса для покупки"
                bot.answer_callback_query(call.id, text)
                return
            else:
                db.remove_item_id(id, 14, 5)
        if resource[0] == 15:
            if db.get_item_invetory(id, 15)['quantity'] < 5:
                text = f"❌ Нехватает ресурса для покупки"
                bot.answer_callback_query(call.id, text)
                return
            else:
                db.remove_item_id(id, 15, 5)


        if not(user_tool):
            db.set_tool(id, int(item['item_id']), int(item['strength']))
            db.edit_money(id, int(item['price']))
            text = f"✅ Куплено: **{item['name']}**"
            bot.answer_callback_query(call.id, text)
            text = f"🚜 *Добро пожаловать в Фермерский магазин!* 🌾\n"\
                    f"Выбери интересующую категорию товаров:"
            bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.shop_kb)
        else:
            text = f'У тебя уже есть грабли\n'\
                    f'{user_tool["name"]} \n'\
                    f'Прочность: {user_tool["strength"]}\n'\
                    f'Хочешь их заменить?'
            bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.replace_rakes_kb)
    else:
        text = f"😢 Упс! Не хватает монет..."
        bot.answer_callback_query(call.id, text)

@bot.callback_query_handler(lambda call: call.data == 'replace_rake')
def replace_rake(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_tool = db.get_rake(id)

    if user['locate'] == 'buy_wood_rake':
        item = db.get_items_id(7)
        resource = [0, 0] # ID ресурса, количество
    if user['locate'] == 'buy_iron_rake':
        item = db.get_items_id(9)
        resource = [0, 0]
    if user['locate'] == 'buy_steel_rake':
        item = db.get_items_id(8)
        resource = [0, 0]
    if user['locate'] == 'buy_rain_rake':
        item = db.get_items_id(10)
        resource = [13, 5]
    if user['locate'] == 'buy_dreams_rake':
        item = db.get_items_id(11)
        resource = [14, 5]
    if user['locate'] == 'buy_quantum_rake':
        item = db.get_items_id(12)
        resource = [15, 5]
    
    if user['money'] >= item['price']:
        if resource[0] == 13:
            if db.get_item_invetory(id, 13)['quantity'] < 5:
                text = f"❌ Нехватает ресурса для покупки"
                bot.answer_callback_query(call.id, text)
                return
            else:
                db.remove_item_id(id, 13, 5)
        if resource[0] == 14:
            if db.get_item_invetory(id, 14)['quantity'] < 5:
                text = f"❌ Нехватает ресурса для покупки"
                bot.answer_callback_query(call.id, text)
                return
            else:
                db.remove_item_id(id, 14, 5)
        if resource[0] == 15:
            if db.get_item_invetory(id, 15)['quantity'] < 5:
                text = f"❌ Нехватает ресурса для покупки"
                bot.answer_callback_query(call.id, text)
                return
            else:
                db.remove_item_id(id, 15, 5)
        
        db.remove_tool(id, user_tool['tool_id'])
        db.set_tool(id, int(item['item_id']), int(item['strength']))
        db.edit_money(id, int(item['price']))
        text = f"✅ Куплено: **{item['name']}**"
        bot.answer_callback_query(call.id, text)
        text = f"🚜 *Добро пожаловать в Фермерский магазин!* 🌾\n"\
                f"Выбери интересующую категорию товаров:"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.shop_kb)
    else:
        text = f"😢 Упс! Не хватает монет..."
        bot.answer_callback_query(call.id, text)


@bot.message_handler(commands=['farm'])
def farm(message):
    id = message.from_user.id
    db = Database()
    user = db.get_me(id)

    if user['locate'] == 'training':
        bot.send_message(id, 
                         "⛔ Пожалуйста, используйте кнопки для прохождения обучения. Вы не можете использовать другие команды сейчас.", 
                         reply_markup=kb.continue_training_kb)
        return
    
    user_farm = db.get_farm(id)
    text = f"🌻 Твоя ферма:\n"\
            f'Выбери грядку, которую ты хочешь обработать'
    bot.send_message(id, text, reply_markup=kb.make_beds(user_farm['amount_beds'])[0])

@bot.callback_query_handler(lambda call: call.data == 'farm')
def farm(call):
    id = call.from_user.id
    db = Database()
    user_farm = db.get_farm(id)
    text = f"🌻 Твоя ферма:\n"\
            f'Выбери грядку, которую ты хочешь обработать'
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.make_beds(user_farm['amount_beds'])[0])

@bot.callback_query_handler(lambda call: call.data == 'buy_bed')
def buy_bed(call):
    id = call.from_user.id 
    db = Database()
    user_farm = db.get_farm(id)
    text = f"🌱 Цена новой грядки: {PRICE_BUY_BEDS[user_farm['amount_beds']]} монет"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.buy_beds_kb)

@bot.callback_query_handler(lambda call: call.data == 'buy_new_bed')
def buy_new_bed(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_farm = db.get_farm(id)
    price = PRICE_BUY_BEDS[user_farm['amount_beds']]

    if user['money'] >= price:
        text = f"🆕 Отличная покупка! Новая грядка добавлена."
        db.edit_farm(id)
        db.set_bed(id, user_farm['amount_beds']+1)
        db.edit_money(id, price)
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_beds)
    else:
        text = f"😢 Упс! Не хватает монет..."
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_beds)

@bot.callback_query_handler(lambda call: call.data == 'beds')
def beds(call):
    id = call.from_user.id
    db = Database()
    user_farm = db.get_farm(id)
    text = f"🌻 Твоя ферма:\n"\
            f'Выбери грядку, которую ты хочешь обработать'
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.make_beds(user_farm['amount_beds'])[0])

@bot.callback_query_handler(lambda call: call.data == 'beds_2')
def beds_2(call):
    id = call.from_user.id
    db = Database()
    user_farm = db.get_farm(id)
    bot.edit_message_reply_markup(id, call.message.message_id, reply_markup=kb.make_beds(user_farm['amount_beds'])[1])

@bot.callback_query_handler(lambda call: call.data == 'bed_1')
def bed_1(call):
    id = call.from_user.id
    db = Database()
    db.edit_locate(id, 'bed_1')
    user_bed = db.get_bed(id, 1)
    user_tool = db.get_rake(id)
    if user_bed['state'] == 3:
        if gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours']) != 0:
            user_bed['state'] = 1
        else:
            db.set_seeds_bed(id, 1, 0, 0, 0, 0)

    text = f"⚔️ [Грядка №1] ⚔️\n"\
            f"▸ 🎯 Лунок: {user_bed['holes']}\n"
    
    if user_tool != None: 
        text += f"🛠️ Грабли: {user_tool['name']} (🛡️ {user_tool['strength']})\n"
    else:
        text += f"🛠️ Грабли: ❌ Нет\n"
    
    if user_bed['state'] == 0:
        text += f"🌱 Состояние: Ничего не посажено\n"\
                f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

    if user_bed['state'] == 1:
        time_left = gl.calculate_end_time(user_bed['time_end'])
        if time_left == True:
            db.set_state_bed(id, 1, 2)
            text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_2_kb)
        else:
            text += f"🌱 Состояние: Посажено\n" \
                    f"🌿 Что растет: {user_bed['name']}\n" \
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_1(time_left))
            
    if user_bed['state'] == 2:
        text += f"✅ Состояние: Можно собирать\n"\
                f"🌱 Что растет: {user_bed['name']}\n"\
                f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_2_kb)
    
    if user_bed['state'] == 3:
        text += f"💀 Состояние: Засохло!\n" \
                f"⚠️ Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

@bot.callback_query_handler(lambda call: call.data == 'bed_2')
def bed_2(call):
    id = call.from_user.id
    db = Database()
    db.edit_locate(id, 'bed_2')
    user_bed = db.get_bed(id, 2)
    user_tool = db.get_rake(id)
    if user_bed['state'] == 3:
        if gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours']) != 0:
            user_bed['state'] = 1
        else:
            db.set_seeds_bed(id, 2, 0, 0, 0, 0)

    text = f"⚔️ [Грядка №2] ⚔️\n"\
            f"▸ 🎯 Лунок: {user_bed['holes']}\n"
    
    if user_tool != None: 
        text += f"🛠️ Грабли: {user_tool['name']} (🛡️ {user_tool['strength']})\n"
    else:
        text += f"🛠️ Грабли: ❌ Нет\n"

    if user_bed['state'] == 0:
        text += f"🌱 Состояние: Ничего не посажено\n"\
                f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

    if user_bed['state'] == 1:
        time_left = gl.calculate_end_time(user_bed['time_end'])
        if time_left == True:
            db.set_state_bed(id, 2, 2)
            text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_2_kb)
        else:
            text += f"🌱 Состояние: Посажено\n" \
                    f"🌿 Что растет: {user_bed['name']}\n" \
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_1(time_left))
            
    if user_bed['state'] == 2:
        text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_2_kb)
    
    if user_bed['state'] == 3:
        text += f"💀 Состояние: Засохло!\n" \
                f"⚠️ Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

@bot.callback_query_handler(lambda call: call.data == 'bed_3')
def bed_3(call):
    id = call.from_user.id
    db = Database()
    db.edit_locate(id, 'bed_3')
    user_bed = db.get_bed(id, 3)
    user_tool = db.get_rake(id)
    if user_bed['state'] == 3:
        if gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours']) != 0:
            user_bed['state'] = 1
        else:
            db.set_seeds_bed(id, 3, 0, 0, 0, 0)

    text = f"⚔️ [Грядка №3] ⚔️\n"\
            f"▸ 🎯 Лунок: {user_bed['holes']}\n"
    
    if user_tool != None: 
        text += f"🛠️ Грабли: {user_tool['name']} (🛡️ {user_tool['strength']})\n"
    else:
        text += f"🛠️ Грабли: ❌ Нет\n"

    if user_bed['state'] == 0:
        text += f"🌱 Состояние: Ничего не посажено\n"\
                f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

    if user_bed['state'] == 1:
        time_left = gl.calculate_end_time(user_bed['time_end'])
        if time_left == True:
            db.set_state_bed(id, 3, 2)
            text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_2_kb)
        else:
            text += f"🌱 Состояние: Посажено\n" \
                    f"🌿 Что растет: {user_bed['name']}\n" \
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_1(time_left))
            
    if user_bed['state'] == 2:
        text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_2_kb)

    if user_bed['state'] == 3:
        text += f"💀 Состояние: Засохло!\n" \
                f"⚠️ Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

@bot.callback_query_handler(lambda call: call.data == 'bed_4')
def bed_4(call):
    id = call.from_user.id
    db = Database()
    db.edit_locate(id, 'bed_4')
    user_bed = db.get_bed(id, 4)
    user_tool = db.get_rake(id)
    if user_bed['state'] == 3:
        if gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours']) != 0:
            user_bed['state'] = 1
        else:
            db.set_seeds_bed(id, 4, 0, 0, 0, 0)

    text = f"⚔️ [Грядка №4] ⚔️\n"\
            f"▸ 🎯 Лунок: {user_bed['holes']}\n"
    
    if user_tool != None: 
        text += f"🛠️ Грабли: {user_tool['name']} (🛡️ {user_tool['strength']})\n"
    else:
        text += f"🛠️ Грабли: ❌ Нет\n"

    if user_bed['state'] == 0:
        text += f"🌱 Состояние: Ничего не посажено\n"\
                f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

    if user_bed['state'] == 1:
        time_left = gl.calculate_end_time(user_bed['time_end'])
        if time_left == True:
            db.set_state_bed(id, 4, 2)
            text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_2_kb)
        else:
            text += f"🌱 Состояние: Посажено\n" \
                    f"🌿 Что растет: {user_bed['name']}\n" \
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_1(time_left))
            
    if user_bed['state'] == 2:
        text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_2_kb)

    if user_bed['state'] == 3:
        text += f"💀 Состояние: Засохло!\n" \
                f"⚠️ Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

@bot.callback_query_handler(lambda call: call.data == 'bed_5')
def bed_5(call):
    id = call.from_user.id
    db = Database()
    db.edit_locate(id, 'bed_5')
    user_bed = db.get_bed(id, 5)
    user_tool = db.get_rake(id)
    if user_bed['state'] == 3:
        if gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours']) != 0:
            user_bed['state'] = 1
        else:
            db.set_seeds_bed(id, 5, 0, 0, 0, 0)

    text = f"⚔️ [Грядка №5] ⚔️\n"\
            f"▸ 🎯 Лунок: {user_bed['holes']}\n"
    
    if user_tool != None: 
        text += f"🛠️ Грабли: {user_tool['name']} (🛡️ {user_tool['strength']})\n"
    else:
        text += f"🛠️ Грабли: ❌ Нет\n"

    if user_bed['state'] == 0:
        text += f"🌱 Состояние: Ничего не посажено\n"\
                f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

    if user_bed['state'] == 1:
        time_left = gl.calculate_end_time(user_bed['time_end'])
        if time_left == True:
            db.set_state_bed(id, 5, 2)
            text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_2_kb)
        else:
            text += f"🌱 Состояние: Посажено\n" \
                    f"🌿 Что растет: {user_bed['name']}\n" \
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_1(time_left))
            
    if user_bed['state'] == 2:
        text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_2_kb)

    if user_bed['state'] == 3:
        text += f"💀 Состояние: Засохло!\n" \
                f"⚠️ Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

@bot.callback_query_handler(lambda call: call.data == 'bed_6')
def bed_6(call):
    id = call.from_user.id
    db = Database()
    db.edit_locate(id, 'bed_6')
    user_bed = db.get_bed(id, 6)
    user_tool = db.get_rake(id)
    if user_bed['state'] == 3:
        if gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours']) != 0:
            user_bed['state'] = 1
        else:
            db.set_seeds_bed(id, 6, 0, 0, 0, 0)

    text = f"⚔️ [Грядка №6] ⚔️\n"\
            f"▸ 🎯 Лунок: {user_bed['holes']}\n"
    
    if user_tool != None: 
        text += f"🛠️ Грабли: {user_tool['name']} (🛡️ {user_tool['strength']})\n"
    else:
        text += f"🛠️ Грабли: ❌ Нет\n"

    if user_bed['state'] == 0:
        text += f"🌱 Состояние: Ничего не посажено\n"\
                f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

    if user_bed['state'] == 1:
        time_left = gl.calculate_end_time(user_bed['time_end'])
        if time_left == True:
            db.set_state_bed(id, 6, 2)
            text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_2_kb)
        else:
            text += f"🌱 Состояние: Посажено\n" \
                    f"🌿 Что растет: {user_bed['name']}\n" \
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_1(time_left))
            
    if user_bed['state'] == 2:
        text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_2_kb)

    if user_bed['state'] == 3:
        text += f"💀 Состояние: Засохло!\n" \
                f"⚠️ Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

@bot.callback_query_handler(lambda call: call.data == 'bed_7')
def bed_7(call):
    id = call.from_user.id
    db = Database()
    db.edit_locate(id, 'bed_7')
    user_bed = db.get_bed(id, 7)
    user_tool = db.get_rake(id)
    if user_bed['state'] == 3:
        if gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours']) != 0:
            user_bed['state'] = 1
        else:
            db.set_seeds_bed(id, 7, 0, 0, 0, 0)

    text = f"⚔️ [Грядка №7] ⚔️\n"\
            f"▸ 🎯 Лунок: {user_bed['holes']}\n"
    
    if user_tool != None: 
        text += f"🛠️ Грабли: {user_tool['name']} (🛡️ {user_tool['strength']})\n"
    else:
        text += f"🛠️ Грабли: ❌ Нет\n"

    if user_bed['state'] == 0:
        text += f"🌱 Состояние: Ничего не посажено\n"\
                f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

    if user_bed['state'] == 1:
        time_left = gl.calculate_end_time(user_bed['time_end'])
        if time_left == True:
            db.set_state_bed(id, 7, 2)
            text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_2_kb)
        else:
            text += f"🌱 Состояние: Посажено\n" \
                    f"🌿 Что растет: {user_bed['name']}\n" \
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_1(time_left))
    if user_bed['state'] == 2:
        text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_2_kb)

    if user_bed['state'] == 3:
        text += f"💀 Состояние: Засохло!\n" \
                f"⚠️ Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

@bot.callback_query_handler(lambda call: call.data == 'bed_8')
def bed_8(call):
    id = call.from_user.id
    db = Database()
    db.edit_locate(id, 'bed_8')
    user_bed = db.get_bed(id, 8)
    user_tool = db.get_rake(id)
    if user_bed['state'] == 3:
        if gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours']) != 0:
            user_bed['state'] = 1
        else:
            db.set_seeds_bed(id, 8, 0, 0, 0, 0)
    
    text = f"⚔️ [Грядка №8] ⚔️\n"\
            f"▸ 🎯 Лунок: {user_bed['holes']}\n"
    
    if user_tool != None: 
        text += f"🛠️ Грабли: {user_tool['name']} (🛡️ {user_tool['strength']})\n"
    else:
        text += f"🛠️ Грабли: ❌ Нет\n"

    if user_bed['state'] == 0:
        text += f"🌱 Состояние: Ничего не посажено\n"\
                f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

    if user_bed['state'] == 1:
        time_left = gl.calculate_end_time(user_bed['time_end'])
        if time_left == True:
            db.set_state_bed(id, 8, 2)
            text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_2_kb)
        else:
            text += f"🌱 Состояние: Посажено\n" \
                    f"🌿 Что растет: {user_bed['name']}\n" \
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_1(time_left))
    if user_bed['state'] == 2:
        text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_2_kb)

    if user_bed['state'] == 3:
        text += f"💀 Состояние: Засохло!\n" \
                f"⚠️ Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

@bot.callback_query_handler(lambda call: call.data == 'bed_9')
def bed_9(call):
    id = call.from_user.id
    db = Database()
    db.edit_locate(id, 'bed_9')
    user_bed = db.get_bed(id, 9)
    user_tool = db.get_rake(id)
    if user_bed['state'] == 3:
        if gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours']) != 0:
            user_bed['state'] = 1
        else:
            db.set_seeds_bed(id, 9, 0, 0, 0, 0)

    text = f"⚔️ [Грядка №9] ⚔️\n"\
            f"▸ 🎯 Лунок: {user_bed['holes']}\n"
    
    if user_tool != None: 
        text += f"🛠️ Грабли: {user_tool['name']} (🛡️ {user_tool['strength']})\n"
    else:
        text += f"🛠️ Грабли: ❌ Нет\n"

    if user_bed['state'] == 0:
        text += f"🌱 Состояние: Ничего не посажено\n"\
                f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

    if user_bed['state'] == 1:
        time_left = gl.calculate_end_time(user_bed['time_end'])
        if time_left == True:
            db.set_state_bed(id, 9, 2)
            text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_2_kb)
        else:
            text += f"🌱 Состояние: Посажено\n" \
                    f"🌿 Что растет: {user_bed['name']}\n" \
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_1(time_left))
            
    if user_bed['state'] == 2:
        text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_2_kb)

    if user_bed['state'] == 3:
        text += f"💀 Состояние: Засохло!\n" \
                f"⚠️ Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

@bot.callback_query_handler(lambda call: call.data == 'bed_10')
def bed_10(call):
    id = call.from_user.id
    db = Database()
    db.edit_locate(id, 'bed_10')
    user_bed = db.get_bed(id, 10)
    user_tool = db.get_rake(id)
    if user_bed['state'] == 3:
        if gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours']) != 0:
            user_bed['state'] = 1
        else:
            db.set_seeds_bed(id, 10, 0, 0, 0, 0)

    text = f"⚔️ [Грядка №10] ⚔️\n"\
            f"▸ 🎯 Лунок: {user_bed['holes']}\n"
    
    if user_tool != None: 
        text += f"🛠️ Грабли: {user_tool['name']} (🛡️ {user_tool['strength']})\n"
    else:
        text += f"🛠️ Грабли: ❌ Нет\n"

    if user_bed['state'] == 0:
        text += f"🌱 Состояние: Ничего не посажено\n"\
                f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)

    if user_bed['state'] == 1:
        time_left = gl.calculate_end_time(user_bed['time_end'])
        if time_left == True:
            db.set_state_bed(id, 10, 2)
            text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_2_kb)
        else:
            text += f"🌱 Состояние: Посажено\n" \
                    f"🌿 Что растет: {user_bed['name']}\n" \
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
            bot.edit_message_text(text, id, call.message.message_id, 
                              reply_markup=kb.bed_state_1(time_left))
            
    if user_bed['state'] == 2:
        text += f"✅ Состояние: Можно собирать\n"\
                    f"🌱 Что растет: {user_bed['name']}\n"\
                    f"💧 Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_2_kb)
    
    if user_bed['state'] == 3:
        text += f"💀 Состояние: Засохло!\n" \
                f"⚠️ Влажность почвы: {gl.calculate_precent_water(user_bed['time_end_watering'], user_bed['watering_hours'])}%"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.bed_state_0_kb)


@bot.callback_query_handler(lambda call: call.data == 'set_seeds')
def set_seeds(call):
    id = call.from_user.id
    db = Database()
    user_locate = db.get_me(id)['locate']
    user_bed = db.get_bed(id, user_locate[4:])
    user_inventory = db.get_item_inventory_type(id, 'семена')
    text = f"🌱 Выбери, что хочешь посадить:\n" \
            f"🔢 Необходимо семян: {user_bed['holes']} шт."
    
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.select_set_seeds(user_inventory, user_locate))
    
@bot.callback_query_handler(lambda call: call.data == 'set_seeds_1')
def set_seeds_1(call):
    id = call.from_user.id 
    db = Database()
    user = db.get_me(id)
    user_farm = db.get_farm(id)
    user_locate = int(db.get_me(id)['locate'][4:])
    user_bed = db.get_bed(id, user_locate)
    user_inventory = db.get_item_invetory(id, 1)
    end_time = gl.end_time(growth_minutes=10)

    if gl.has_time_passed(user['buster_x10_time_all']):
        end_time = gl.end_time(growth_minutes=1)

    if user_inventory['quantity'] >= user_bed['holes']:
        if gl.random_chance_resistance(user_bed['chance_resistance']) and user_farm != 29:
            db.set_seeds_bed(id, user_locate, 1, 1, end_time, 1)
        else:
            db.set_seeds_bed(id, user_locate, 1, 1, end_time, 0)

        if user_farm['buster'] == 29:
            db.set_seeds_bed(id, user_locate, 1, 1, end_time, 0)
            db.used_buster(id, 0)

        if gl.compare_times(str(user_bed['time_end_watering']), str(db.get_bed(id, user_locate)['time_end'])):
            db.set_state_bed(id, user_locate, 3)

        db.remove_item_id(id, 1, user_bed['holes'])
        text = f"🪴 {user_inventory['name']} успешно посажены!\n" 
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_beds)
    else:
        text = f"❌ Тебе не хватает семян!\n" \
                f"Нужно докупить или выбрать другую культуру"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_select_set_seeds)

@bot.callback_query_handler(lambda call: call.data == 'set_seeds_2')
def set_seeds_2(call):
    id = call.from_user.id 
    db = Database()
    user = db.get_me(id)
    user_farm = db.get_farm(id)
    user_locate = int(db.get_me(id)['locate'][4:])
    user_bed = db.get_bed(id, user_locate)
    user_inventory = db.get_item_invetory(id, 2)
    end_time = gl.end_time(growth_minutes=20)

    if gl.has_time_passed(user['buster_x10_time_all']):
        end_time = gl.end_time(growth_minutes=2)

    if user_inventory['quantity'] >= user_bed['holes']:
        if gl.random_chance_resistance(user_bed['chance_resistance']) and user_farm != 29:
            db.set_seeds_bed(id, user_locate, 1, 2, end_time, 1)
        else:
            db.set_seeds_bed(id, user_locate, 1, 2, end_time, 0)

        if user_farm['buster'] == 29:
            db.set_seeds_bed(id, user_locate, 1, 2, end_time, 0)
            db.used_buster(id, 0)

        if gl.compare_times(str(user_bed['time_end_watering']), str(db.get_bed(id, user_locate)['time_end'])):
            db.set_state_bed(id, user_locate, 3)

        db.remove_item_id(id, 2, user_bed['holes'])
        text = f"🪴 {user_inventory['name']} успешно посажены!\n"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_beds)
    else:
        text = f"❌ Тебе не хватает семян!\n" \
                f"Нужно докупить или выбрать другую культуру"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_select_set_seeds)

@bot.callback_query_handler(lambda call: call.data == 'set_seeds_3')
def set_seeds_3(call):
    id = call.from_user.id 
    db = Database()
    user = db.get_me(id)
    user_farm = db.get_farm(id)
    user_locate = int(db.get_me(id)['locate'][4:])
    user_bed = db.get_bed(id, user_locate)
    user_inventory = db.get_item_invetory(id, 3)
    end_time = gl.end_time(growth_minutes=30)

    if gl.has_time_passed(user['buster_x10_time_all']):
        end_time = gl.end_time(growth_minutes=3)

    if user_inventory['quantity'] >= user_bed['holes']:
        if gl.random_chance_resistance(user_bed['chance_resistance']) and user_farm != 29:
            db.set_seeds_bed(id, user_locate, 1, 3, end_time, 1)
        else:
            db.set_seeds_bed(id, user_locate, 1, 3, end_time, 0)

        if user_farm['buster'] == 29:
            db.set_seeds_bed(id, user_locate, 1, 3, end_time, 0)
            db.used_buster(id, 0)

        if gl.compare_times(str(user_bed['time_end_watering']), str(db.get_bed(id, user_locate)['time_end'])):
            db.set_state_bed(id, user_locate, 3)

        db.remove_item_id(id, 3, user_bed['holes'])
        text = f"🪴 {user_inventory['name']} успешно посажены!\n"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_beds)
    else:
        text = f"❌ Тебе не хватает семян!\n" \
                f"Нужно докупить или выбрать другую культуру"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_select_set_seeds)

@bot.callback_query_handler(lambda call: call.data == 'set_seeds_4')
def set_seeds_4(call):
    id = call.from_user.id 
    db = Database()
    user = db.get_me(id)
    user_farm = db.get_farm(id)
    user_locate = int(db.get_me(id)['locate'][4:])
    user_bed = db.get_bed(id, user_locate)
    user_inventory = db.get_item_invetory(id, 4)
    end_time = gl.end_time(growth_minutes=45)

    if gl.has_time_passed(user['buster_x10_time_all']):
        end_time = gl.end_time(growth_minutes=5)

    if user_inventory['quantity'] >= user_bed['holes']:
        if gl.random_chance_resistance(user_bed['chance_resistance']) and user_farm != 29:
            db.set_seeds_bed(id, user_locate, 1, 4, end_time, 1)
        else:
            db.set_seeds_bed(id, user_locate, 1, 4, end_time, 0)

        if user_farm['buster'] == 29:
            db.set_seeds_bed(id, user_locate, 1, 4, end_time, 0)
            db.used_buster(id, 0)

        if gl.compare_times(str(user_bed['time_end_watering']), str(db.get_bed(id, user_locate)['time_end'])):
            db.set_state_bed(id, user_locate, 3)

        db.remove_item_id(id, 4, user_bed['holes'])
        text = f"🪴 {user_inventory['name']} успешно посажены!\n"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_beds)
    else:
        text = f"❌ Тебе не хватает семян!\n" \
                f"Нужно докупить или выбрать другую культуру"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_select_set_seeds)

@bot.callback_query_handler(lambda call: call.data == 'set_seeds_5')
def set_seeds_5(call):
    id = call.from_user.id 
    db = Database()
    user = db.get_me(id)
    user_farm = db.get_farm(id)
    user_locate = int(db.get_me(id)['locate'][4:])
    user_bed = db.get_bed(id, user_locate)
    user_inventory = db.get_item_invetory(id, 5)
    end_time = gl.end_time(growth_hours=4)

    if gl.has_time_passed(user['buster_x10_time_all']):
        end_time = gl.end_time(growth_minutes=24)

    if user_inventory['quantity'] >= user_bed['holes']:
        if gl.random_chance_resistance(user_bed['chance_resistance']) and user_farm != 29:
            db.set_seeds_bed(id, user_locate, 1, 5, end_time, 1)
        else:
            db.set_seeds_bed(id, user_locate, 1, 5, end_time, 0)

        if user_farm['buster'] == 29:
            db.set_seeds_bed(id, user_locate, 1, 5, end_time, 0)
            db.used_buster(id, 0)

        if gl.compare_times(str(user_bed['time_end_watering']), str(db.get_bed(id, user_locate)['time_end'])):
            db.set_state_bed(id, user_locate, 3)

        db.remove_item_id(id, 5, user_bed['holes'])
        text = f"🪴 {user_inventory['name']} успешно посажены!\n"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_beds)
    else:
        text = f"❌ Тебе не хватает семян!\n" \
                f"Нужно докупить или выбрать другую культуру"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_select_set_seeds)

@bot.callback_query_handler(lambda call: call.data == 'set_seeds_6')
def set_seeds_6(call):
    id = call.from_user.id 
    db = Database()
    user = db.get_me(id)
    user_farm = db.get_farm(id)
    user_locate = int(db.get_me(id)['locate'][4:])
    user_bed = db.get_bed(id, user_locate)
    user_inventory = db.get_item_invetory(id, 6)
    end_time = gl.end_time(growth_hours=2, growth_minutes=30)

    if gl.has_time_passed(user['buster_x10_time_all']):
        end_time = gl.end_time(growth_minutes=15)

    if user_inventory['quantity'] >= user_bed['holes']:
        if gl.random_chance_resistance(user_bed['chance_resistance']):
            db.set_seeds_bed(id, user_locate, 1, 6, end_time, 1)
        else:
            db.set_seeds_bed(id, user_locate, 1, 6, end_time, 0)

        if user_farm['buster'] == 29:
            db.set_seeds_bed(id, user_locate, 1, 6, end_time, 0)
            db.used_buster(id, 0)
        
        if gl.compare_times(str(user_bed['time_end_watering']), str(db.get_bed(id, user_locate)['time_end'])):
            db.set_state_bed(id, user_locate, 3)

        db.remove_item_id(id, 6, user_bed['holes'])
        text = f"🪴 {user_inventory['name']} успешно посажены!\n"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_beds)
    else:
        text = f"❌ Тебе не хватает семян!\n" \
                f"Нужно докупить или выбрать другую культуру"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_select_set_seeds)

@bot.callback_query_handler(lambda call: call.data == 'get_harvest')
def get_harvest(call):
    id = call.from_user.id
    db = Database()
    user_farm = db.get_farm(id)
    user_tool = db.get_tool_rake(id)
    user_locate = db.get_me(id)['locate']
    user_bed = db.get_bed(id, int(user_locate[4:]))
    item_harvest = db.get_items_id(HARVEST[user_bed['id_planted']])
    resource = gl.random_resource()
    tasks = db.get_tasks(id)


    if user_tool == None:
        text = f"🚫 Ошибка: Нет граблей!\n" \
                f"Чтобы собрать урожай, тебе нужны грабли"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_get_harvest(user_locate))
        return
    else:
        user_tool = user_tool['tool_id']
        db.set_seeds_bed(id, int(user_locate[4:]), 0, 0, '0', 0)
        if user_bed['resistance'] == 1:
            text = f"💀 Почва заболела - урожай погиб!\n" \
                    f"😢 Очень жаль, но ничего не выросло..."
            bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_get_harvest(user_locate))
            return
        else:
            if user_farm['buster'] == 28:
                buster = 2
                db.used_buster(id, 0)
            else:
                buster = 1
            quantity = 0
            if user_tool == 7:
                quantity = int(user_bed['holes'])
                text = f"✨ Урожай! ✨\nСобрано {quantity*buster} {item_harvest['name']}"
                db.set_inventory(id, item_harvest['item_id'], quantity*buster)
                bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_get_harvest(user_locate))
            if user_tool == 8:
                quantity = int(user_bed['holes']) + 3
                text = f"✨ Урожай! ✨\nСобрано {quantity*buster} {item_harvest['name']}"
                db.set_inventory(id, item_harvest['item_id'], quantity*buster)
                bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_get_harvest(user_locate))
            if user_tool == 9:
                quantity = int(user_bed['holes']) + 2
                text = f"✨ Урожай! ✨\nСобрано {quantity*buster} {item_harvest['name']}"
                db.set_inventory(id, item_harvest['item_id'], quantity*buster)
                bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_get_harvest(user_locate))
            if user_tool == 10:
                quantity = int(user_bed['holes'])
                text = f"✨ Урожай! ✨\nСобрано {quantity*buster} {item_harvest['name']}"
                db.set_inventory(id, item_harvest['item_id'], quantity*buster)
                bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_get_harvest(user_locate))
            if user_tool == 11:
                if gl.is_night_time():
                    quantity = int(user_bed['holes'])*2
                else:
                    quantity = int(user_bed['holes'])
                text = f"✨ Урожай! ✨\nСобрано {quantity*buster} {item_harvest['name']}"
                db.set_inventory(id, item_harvest['item_id'], quantity*buster)
                bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_get_harvest(user_locate))
            if user_tool == 12:
                if gl.random_chance():
                    quantity = int(user_bed['holes'])*2
                    text = f"✨ Урожай! ✨\nСобрано {quantity*buster} {item_harvest['name']}"
                    db.set_inventory(id, item_harvest['item_id'], quantity*buster)
                    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_get_harvest(user_locate))
                else:
                    quantity = int(user_bed['holes'])
                    text = f"✨ Урожай! ✨\nСобрано {quantity*buster} {item_harvest['name']}"
                    db.set_inventory(id, item_harvest['item_id'], quantity*buster)
                    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_get_harvest(user_locate))
            if resource != None:
                resource_info = db.get_items_id(resource)
                text_2 = f"✨ Удача! При сборе урожая ты нашёл:\n" \
                        f"1 {resource_info['name']} (редкий ресурс!)"
                bot.answer_callback_query(call.id, text_2)
                db.set_inventory(id, resource)

            db.edit_tool(id, user_tool)

            if tasks['plant1'] == item_harvest['item_id'] and tasks['task1_completed'] != -1:
                db.update_completed_task(id, 1, quantity*buster)
            if tasks['plant2'] == item_harvest['item_id'] and tasks['task2_completed'] != -1:
                db.update_completed_task(id, 2, quantity*buster)

@bot.callback_query_handler(lambda call: call.data == 'watering')
def watering(call):
    id = call.from_user.id 
    db = Database()
    user_farm = db.get_farm(id)
    user_locate = db.get_me(id)['locate']
    user_bed = db.get_bed(id, user_locate[4:])
    user_tool = db.get_tool_rake(id)

    text = f'Ты успешно полил грядку'
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_get_harvest(user_locate))

    if user_farm['buster'] == 27:
        db.watering_bed(id, user_locate[4:], gl.end_time(24))
        db.used_buster(id, 0)
        return
    if user_tool != None:
        if user_tool['tool_id'] == 10:
            db.watering_bed(id, user_locate[4:], gl.end_time(int(user_bed['watering_hours'])*2))
            return
    
    db.watering_bed(id, user_locate[4:], gl.end_time(user_bed['watering_hours']))
        
    if user_bed['state'] == 3:
        db.set_state_bed(id, user_locate[4:], 1)



@bot.callback_query_handler(lambda call: call.data == 'upgrade_bed')
def upgrade_bed(call):
    id = call.from_user.id 
    db = Database()
    user_locate = db.get_me(id)['locate']
    text = f"🛠️ Выбери улучшение:\n"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.upgrade_bed(user_locate))


@bot.callback_query_handler(lambda call: call.data == 'disease_resistance')
def disease_resistance(call):
    id = call.from_user.id
    db = Database()
    user_locate = db.get_me(id)['locate']
    user_bed = db.get_bed(id, user_locate[4:])
    items_for_upgrade = PRICE_UPGRADE_DISEASE_RESISTANCE[user_bed['chance_resistance']]
    text = f"🌱 ИММУНИТЕТ ГРЯДКИ 🌱\n\n"\
            f"Текущая защита: \n"\
            f"☣️ Риск болезни: {user_bed['chance_resistance']}%\n"\
            f"➡ После улучшения: {user_bed['chance_resistance']-1}%\n\n"\
            f"📦 Необходимые ресурсы:\n"\
            f"💰 {items_for_upgrade[0]} монет\n"\
            f"🌿 {items_for_upgrade[1]} лечебной травы\n\n"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.disease_resistance_kb)

@bot.callback_query_handler(lambda call: call.data == 'upgrade_disease_resistance')
def upgrade_disease_resistance(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_inventory = db.get_item_invetory(id, 22)
    user_bed = db.get_bed(id, user['locate'][4:])
    items_for_upgrade = PRICE_UPGRADE_DISEASE_RESISTANCE[user_bed['chance_resistance']]

    if user_inventory == None:
        user_inventory = {'quantity': 0}

    if user['money'] >= items_for_upgrade[0] and user_inventory['quantity'] >= items_for_upgrade[1]:
        text = f'"Грядка улучшена! ✔️🌱"'
        db.upgrade_disease_resistance(id, user['locate'][4:])
        db.edit_money(id, items_for_upgrade[0])
        db.remove_item_id(id, 22, items_for_upgrade[1])
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_to_upgrade_kb)
    else:
        text = f"😢 Упс! Не хватает монет или ресурсов..."
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_to_upgrade_kb)

@bot.callback_query_handler(lambda call: call.data == 'reducing_soil')
def reducing_soil(call):
    id = call.from_user.id
    db = Database()
    user_locate = db.get_me(id)['locate']
    user_bed = db.get_bed(id, user_locate[4:])
    items_for_upgrade = PRICE_UPGRADE_TIME_WATERING[user_bed['watering_hours']]
    text = f"🔧 Модернизация полива\n"\
            f"────────────────────\n"\
            f"Текущие параметры:\n"\
            f"Длительность: {user_bed['watering_hours']} ч\n\n"\
            f"После апгрейда:\n"\
            f"Длительность: +1 ч (всего {user_bed['watering_hours']+1} ч)\n\n"\
            f"Компоненты для улучшения:\n"\
            f"▸ {items_for_upgrade[0]} монет\n"\
            f"▸ {items_for_upgrade[1]} молекул воды"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.reducing_soil_kb)
    
@bot.callback_query_handler(lambda call: call.data == 'upgrade_reducing_soil')
def upgrade_reducing_soil(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_inventory = db.get_item_invetory(id, 13)
    user_bed = db.get_bed(id, user['locate'][4:])
    items_for_upgrade = PRICE_UPGRADE_TIME_WATERING[user_bed['watering_hours']]

    if user_inventory == None:
        user_inventory = {'quantity': 0}

    if user['money'] >= items_for_upgrade[0] and user_inventory['quantity'] >= items_for_upgrade[1]:
        text = f'"Грядка улучшена! ✔️🌱"'
        db.upgrade_disease_resistance(id, user['locate'][4:])
        db.edit_money(id, items_for_upgrade[0])
        db.remove_item_id(id, 13, items_for_upgrade[1])
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_to_upgrade_kb)
    else:
        text = f"😢 Упс! Не хватает монет или ресурсов..."
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_to_upgrade_kb)


@bot.callback_query_handler(lambda call: call.data == 'up_number_holes')
def up_number_holes(call):
    id = call.from_user.id
    db = Database()
    user_money = db.get_me(id)['money']
    user_locate = db.get_me(id)['locate']
    user_bed = db.get_bed(id, user_locate[4:])
    text =  f"➕ Дополнительная лунка\n"\
            f"💵 Цена: {round(user_bed['last_price_added_holes']*1.1)}\n"\
            f"👛 Ваш баланс: {user_money}\n"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.added_holes_kb)


@bot.callback_query_handler(lambda call: call.data == 'added_holes')
def added_holes(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_bed = db.get_bed(id, user['locate'][4:])
    price = round(user_bed['last_price_added_holes']*1.1)

    if user['money'] >= price:
        text = f'"Грядка улучшена! ✔️🌱"'
        db.added_holes(id, user['locate'][4:], price)
        db.edit_money(id, price)
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_to_upgrade_kb)
    else:
        text = f"😢 Упс! Не хватает монет..."
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_to_upgrade_kb)


@bot.callback_query_handler(lambda call: call.data == 'box')
def box(call):
    id = call.from_user.id 
    db = Database()
    user_inventory = db.get_item_inventory_type(id, 'бокс')
    text = f'🎁Выбери какой бокс хочешь открыть:'
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.open_box(user_inventory))

@bot.callback_query_handler(lambda call: call.data == 'box_23')
def box_23(call):
    id = call.from_user.id 
    db = Database()
    text =  f"📦 *ОБЫЧНЫЙ ЯЩИК* 📦\n"\
            f"▫️ Монеты: 50-100\n"\
            f"▫️ Пшеница: 2-5\n"\
            f"▫️ Мокровь: 2-5\n"\
            f"▫️ Кукуруза: 2-5\n"\
            f"▫️ Картофель: 2-5\n"
    db.edit_locate(id, 'box_23')
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.open_box_kb)

@bot.callback_query_handler(lambda call: call.data == 'box_24')
def box_24(call):
    id = call.from_user.id 
    db = Database()
    text = f"🔮 *РЕДКИЙ ЯЩИК* 🔮\n"\
            f"▫️ Монеты: 100-200\n"\
            f"▫️ Кукуруза: 5-10\n"\
            f"▫️ Картофель: 5-10\n"\
            f"▫️ Лунный лотос: 1-2\n"\
            f"▫️ Огненный перец: 1-2"
    db.edit_locate(id, 'box_24')
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.open_box_kb)

@bot.callback_query_handler(lambda call: call.data == 'box_25')
def box_25(call):
    id = call.from_user.id 
    db = Database()
    text = f"💎 *ЭПИЧЕСКИЙ ЯЩИК* 💎\n"\
            f"▫️ Монеты: 300-500\n"\
            f"▫️ Лечебная трава: 1-2\n"\
            f"▫️ Молекула дождя: 1-2\n"\
            f"▫️ Сновиденческая трава: 1-2\n"\
            f"▫️ Квантовый обломок: 1-2"
    db.edit_locate(id, 'box_25')
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.open_box_kb)

@bot.callback_query_handler(lambda call: call.data == 'box_26')
def box_26(call):
    id = call.from_user.id 
    db = Database()
    text = f"✨ *ЛЕГЕНДАРНЫЙ ЯЩИК* ✨\n"\
            f"▫️ Монеты: 1000-1500\n"\
            f"▫️ Бустер 'Отказ от воды': 1\n"\
            f"▫️ Бустер 'Удвоенный урожай': 1\n"\
            f"▫️ Бустер 'Отсутствие болезней': 1\n"\
            f"▫️ Золотая монета: 1-10"
    db.edit_locate(id, 'box_26')
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.open_box_kb)


@bot.callback_query_handler(lambda call: call.data == 'open_box')
def open_box(call):
    id = call.from_user.id 
    db = Database()
    user_locate = db.get_me(id)['locate']
    box = gl.open_box(int(user_locate[4:]))
    
    if box['id'] != 0 and box['id'] != -1:
        db.set_inventory(id, box['id'], box['quantity'])
    if box['id'] == -1:
        db.add_gold_money(id, box['quantity'])
    if box['id'] == 0:
        db.add_money(id, box['quantity'])

    db.remove_item_id(id, int(user_locate[4:]), 1)

    text = f"✨━━━━━━━━━━━━━━━━━━━━✨\n"\
            f"      🎉 ТВОЯ НАГРАДА! 🎉\n"\
            f"✨━━━━━━━━━━━━━━━━━━━✨\n"\
            f"🎁 {box['item']} ×{box['quantity']}\n"\
            f"✨━━━━━━━━━━━━━━━━━━━✨"
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_box_kb)


@bot.callback_query_handler(lambda call: call.data == 'busters')
def busters(call):
    id = call.from_user.id
    db = Database()
    user_farm = db.get_farm(id)
    buster = db.get_item_inventory_type(id, 'бустер')
    text = f'✨ Твои бустеры  \n'
    if user_farm['buster'] != 0:
        info_buster = db.get_items_id(user_farm['buster'])
        text += f'✅ Активирован: {info_buster["name"]}'
    else:
        text += f'❌ Нет активных бустеров  '
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.busters(buster))


@bot.callback_query_handler(lambda call: call.data == 'buster_27')
def buster_27(call):
    id = call.from_user.id
    db = Database()
    text = f'💧 Бустер «Отказ от воды»  \n'\
            f'☀️ Ваша грядка под защитой\n'\
            f'⏳ Целые сутки без забот!'
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.used_buster_kb)
    db.edit_locate(id, 'buster_27')

@bot.callback_query_handler(lambda call: call.data == 'buster_28')
def buster_28(call):
    id = call.from_user.id
    db = Database()
    text = f'🌾 Бустер «Удвоенный урожай» \n'\
            f'✧ Следующий сбор принесёт 2x урожая!'
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.used_buster_kb)
    db.edit_locate(id, 'buster_28')

@bot.callback_query_handler(lambda call: call.data == 'buster_29')
def buster_29(call):
    id = call.from_user.id
    db = Database()
    text = f'🌿 Бустер «Иммунитет» \n'\
            f'✧ Следующая посадка защищена от болезней!'
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.used_buster_kb)
    db.edit_locate(id, 'buster_29')

@bot.callback_query_handler(lambda call: call.data == 'used_buster')
def used_buster(call):
    id = call.from_user.id
    db = Database()
    user_farm = db.get_farm(id)
    user_locate = db.get_me(id)['locate']
    info_buster = db.get_items_id(int(user_locate[7:]))
    if user_farm['buster'] == 0:
        db.used_buster(id, info_buster['item_id'])
        db.remove_item_id(id, info_buster['item_id'])
        text = f'✅Ты использовал {info_buster["name"]}'
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_busters_kb)
    else:
        text = f'❌Ты уже используешь бустер'
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_busters_kb)


@bot.callback_query_handler(lambda call: call.data == 'casino')
def casino(call):
    id = call.from_user.id
    text = f'🎰Ты попал в казино\nЗа какой стол сядешь? '
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.casino_kb)

@bot.callback_query_handler(lambda call: call.data == 'casino_back')
def casino_back(call):
    id = call.from_user.id
    text = f'🎰Ты попал в казино\nЗа какой стол сядешь? '
    bot.delete_message(id, call.message.message_id)
    bot.send_message(id, text, reply_markup=kb.casino_kb)


@bot.callback_query_handler(lambda call: call.data == 'roulette')
def roulette(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    if user['money'] < 10:
        text = '❌ Тебе нехватает на минимальную ставку в 10 монет'
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_casino_kb)
    else:
        db.set_casino(id)
        user_casino = db.get_casino(id)
        text = f"💰 *Текущая ставка* 💰\n"\
                f"══════════════════\n"\
                f"🔘 Поставлено: {user_casino['bid']}\n"\
                f"💳 Доступно: {user['money']}\n"\
                f"══════════════════\n"
        photo = open('image/roulette.png', 'rb')
        bot.delete_message(id, call.message.message_id)
        bot.send_photo(id, photo, text, reply_markup=kb.roulette_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_user_d2')
def bid_user_d2(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    if user_casino['bid'] / 2 < 10:
        text = '❌ Ставка не может быть меньше 10 монет'
        bot.answer_callback_query(call.id, text)
    else:
        db.update_bid(id, user_casino['bid'], '/ 2')
        user_casino = db.get_casino(id)
        text = f"💰 *Текущая ставка* 💰\n"\
                f"══════════════════\n"\
                f"🔘 Поставлено: {user_casino['bid']}\n"\
                f"💳 Доступно: {user['money']}\n"\
                f"══════════════════\n"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_user_d10')
def bid_user_d10(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    if user_casino['bid'] / 10 < 10:
        text = '❌ Ставка не может быть меньше 10 монет'
        bot.answer_callback_query(call.id, text)
    else:
        db.update_bid(id, user_casino['bid'], '/ 10')
        user_casino = db.get_casino(id)
        text = f"💰 *Текущая ставка* 💰\n"\
                f"══════════════════\n"\
                f"🔘 Поставлено: {user_casino['bid']}\n"\
                f"💳 Доступно: {user['money']}\n"\
                f"══════════════════\n"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_user_x2')
def bid_user_x2(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    if user['money'] < user_casino['bid'] * 2:
        text = f'❌ У тебя нехватает денег на повышение ставки'
        bot.answer_callback_query(call.id, text)
    else:
        db.update_bid(id, user_casino['bid'], '* 2')
        user_casino = db.get_casino(id)
        text = f"💰 *Текущая ставка* 💰\n"\
                f"══════════════════\n"\
                f"🔘 Поставлено: {user_casino['bid']}\n"\
                f"💳 Доступно: {user['money']}\n"\
                f"══════════════════\n"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_user_x10')
def bid_user_x10(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    if user['money'] < user_casino['bid'] * 10:
        text = f'❌ У тебя нехватает денег на повышение ставки'
        bot.answer_callback_query(call.id, text)
    else:
        db.update_bid(id, user_casino['bid'], '* 10')
        user_casino = db.get_casino(id)
        text = f"💰 *Текущая ставка* 💰\n"\
                f"══════════════════\n"\
                f"🔘 Поставлено: {user_casino['bid']}\n"\
                f"💳 Доступно: {user['money']}\n"\
                f"══════════════════\n"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)


@bot.callback_query_handler(lambda call: call.data == 'bid_1_12')
def bid_1_12(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    number = gl.roulette_random()
    
    if user['money'] < user_casino['bid'] or user['money'] < 10:
        text = f"😢 Упс! Не хватает монет..."
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.back_casino_kb)
        return

    text = f'Выпало число {number}\n\n'
    if number >= 1 and number <= 12:
        db.add_money(id, user_casino['bid']*2)
        user = db.get_me(id)
        text += f"＋ Выиграно: {user_casino['bid']*3} ＋\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)
    else:
        db.edit_money(id, user_casino['bid'])
        user = db.get_me(id)
        text += f"― Проиграно: {user_casino['bid']} ―\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_13_24')
def bid_13_24(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    number = gl.roulette_random()
    
    if user['money'] < user_casino['bid'] or user['money'] < 10:
        text = f"😢 Упс! Не хватает монет..."
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.back_casino_kb)
        return

    text = f'Выпало число {number}\n\n'
    if number >= 13 and number <= 24:
        db.add_money(id, user_casino['bid']*2)
        user = db.get_me(id)
        text += f"＋ Выиграно: {user_casino['bid']*3} ＋\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)
    else:
        db.edit_money(id, user_casino['bid'])
        user = db.get_me(id)
        text += f"― Проиграно: {user_casino['bid']} ―\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_25_36')
def bid_25_36(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    number = gl.roulette_random()
    
    if user['money'] < user_casino['bid'] or user['money'] < 10:
        text = f"😢 Упс! Не хватает монет..."
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.back_casino_kb)
        return

    text = f'Выпало число {number}\n\n'
    if number >= 25 and number <= 36:
        db.add_money(id, user_casino['bid']*2)
        user = db.get_me(id)
        text += f"＋ Выиграно: {user_casino['bid']*3} ＋\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)
    else:
        db.edit_money(id, user_casino['bid'])
        user = db.get_me(id)
        text += f"― Проиграно: {user_casino['bid']} ―\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_black')
def bid_black(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    number = gl.roulette_random()

    if user['money'] < user_casino['bid'] or user['money'] < 10:
        text = f"😢 Упс! Не хватает монет..."
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.back_casino_kb)
        return

    text = f'Выпало число {number}\n\n'
    if number in [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]:
        db.add_money(id, user_casino['bid'])
        user = db.get_me(id)
        text += f"＋ Выиграно: {user_casino['bid']*2} ＋\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)
    else:
        db.edit_money(id, user_casino['bid'])
        user = db.get_me(id)
        text += f"― Проиграно: {user_casino['bid']} ―\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_red')
def bid_red(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    number = gl.roulette_random()

    if user['money'] < user_casino['bid'] or user['money'] < 10:
        text = f"😢 Упс! Не хватает монет..."
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.back_casino_kb)
        return

    text = f'Выпало число {number}\n\n'
    if number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
        db.add_money(id, user_casino['bid'])
        user = db.get_me(id)
        text += f"＋ Выиграно: {user_casino['bid']*2} ＋\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)
    else:
        db.edit_money(id, user_casino['bid'])
        user = db.get_me(id)
        text += f"― Проиграно: {user_casino['bid']} ―\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_even')
def bid_even(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    number = gl.roulette_random()

    if user['money'] < user_casino['bid'] or user['money'] < 10:
        text = f"😢 Упс! Не хватает монет..."
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.back_casino_kb)
        return

    text = f'Выпало число {number}\n\n'
    if number % 2 == 0 and number != 0:
        db.add_money(id, user_casino['bid'])
        user = db.get_me(id)
        text += f"＋ Выиграно: {user_casino['bid']*2} ＋\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)
    else:
        db.edit_money(id, user_casino['bid'])
        user = db.get_me(id)
        text += f"― Проиграно: {user_casino['bid']} ―\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_odd')
def bid_odd(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    number = gl.roulette_random()

    if user['money'] < user_casino['bid'] or user['money'] < 10:
        text = f"😢 Упс! Не хватает монет..."
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.back_casino_kb)
        return

    text = f'Выпало число {number}\n\n'
    if number % 2 == 1:
        db.add_money(id, user_casino['bid'])
        user = db.get_me(id)
        text += f"＋ Выиграно: {user_casino['bid']*2} ＋\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)
    else:
        db.edit_money(id, user_casino['bid'])
        user = db.get_me(id)
        text += f"― Проиграно: {user_casino['bid']} ―\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_zero')
def bid_zero(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    number = gl.roulette_random()

    if user['money'] < user_casino['bid'] or user['money'] < 10:
        text = f"😢 Упс! Не хватает монет..."
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.back_casino_kb)
        return

    text = f'Выпало число {number}\n\n'
    if number == 0:
        db.add_money(id, user_casino['bid']*35)
        user = db.get_me(id)
        text += f"＋ Выиграно: {user_casino['bid']*36} ＋\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)
    else:
        db.edit_money(id, user_casino['bid'])
        user = db.get_me(id)
        text += f"― Проиграно: {user_casino['bid']} ―\n" \
                f"Твоя ставка {user_casino['bid']} монет\n"\
                f"💰 {user['money']}"
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.roulette_kb)



@bot.callback_query_handler(lambda call: call.data == 'dice')
def dice(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    if user['money'] < 10:
        text = 'Тебе нехватает на минимальную ставку в 10 монет'
        bot.delete_message(id, call.message.message_id)
        bot.send_message(id, text, reply_markup=kb.back_casino_kb)
    else:
        db.set_casino(id)
        user_casino = db.get_casino(id)
        text = f"💰 *Текущая ставка* 💰\n"\
                f"══════════════════\n"\
                f"🔘 Поставлено: {user_casino['bid']}\n"\
                f"💳 Доступно: {user['money']}\n"\
                f"══════════════════\n"
        bot.delete_message(id, call.message.message_id)
        bot.send_message(id, text, reply_markup=kb.dice_kb)

@bot.callback_query_handler(lambda call: call.data == 'dice_back')
def dice(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    if user['money'] < 10:
        text = 'Тебе нехватает на минимальную ставку в 10 монет'
        bot.delete_message(id, call.message.message_id)
        bot.send_message(id, text, reply_markup=kb.back_casino_kb)
    else:
        user_casino = db.get_casino(id)
        text = f"💰 *Текущая ставка* 💰\n"\
                f"══════════════════\n"\
                f"🔘 Поставлено: {user_casino['bid']}\n"\
                f"💳 Доступно: {user['money']}\n"\
                f"══════════════════\n"
        bot.delete_message(id, call.message.message_id)
        bot.send_message(id, text, reply_markup=kb.dice_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_user_dice_d2')
def bid_user_dice_d2(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    if user_casino['bid'] / 2 < 10:
        text = 'Ставка не может быть меньше 10 монет'
        bot.answer_callback_query(call.id, text)
    else:
        db.update_bid(id, user_casino['bid'], '/ 2')
        user_casino = db.get_casino(id)
        text = f"💰 *Текущая ставка* 💰\n"\
                f"══════════════════\n"\
                f"🔘 Поставлено: {user_casino['bid']}\n"\
                f"💳 Доступно: {user['money']}\n"\
                f"══════════════════\n"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.dice_kb)
    
@bot.callback_query_handler(lambda call: call.data == 'bid_user_dice_d10')
def bid_user_dice_d10(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    if user_casino['bid'] / 10 < 10:
        text = 'Ставка не может быть меньше 10 монет'
        bot.answer_callback_query(call.id, text)
    else:
        db.update_bid(id, user_casino['bid'], '/ 10')
        user_casino = db.get_casino(id)
        text = f"💰 *Текущая ставка* 💰\n"\
                f"══════════════════\n"\
                f"🔘 Поставлено: {user_casino['bid']}\n"\
                f"💳 Доступно: {user['money']}\n"\
                f"══════════════════\n"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.dice_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_user_dice_x2')
def bid_user_dice_x2(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    if user['money'] < user_casino['bid'] * 2:
        text = f'У тебя нехватает денег на повышение ставки'
        bot.answer_callback_query(call.id, text)
    else:
        db.update_bid(id, user_casino['bid'], '* 2')
        user_casino = db.get_casino(id)
        text = f"💰 *Текущая ставка* 💰\n"\
                f"══════════════════\n"\
                f"🔘 Поставлено: {user_casino['bid']}\n"\
                f"💳 Доступно: {user['money']}\n"\
                f"══════════════════\n"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.dice_kb)

@bot.callback_query_handler(lambda call: call.data == 'bid_user_dice_x10')
def bid_user_dice_x10(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    if user['money'] < user_casino['bid'] * 10:
        text = f'У тебя нехватает денег на повышение ставки'
        bot.answer_callback_query(call.id, text)
    else:
        db.update_bid(id, user_casino['bid'], '* 10')
        user_casino = db.get_casino(id)
        text = f"💰 *Текущая ставка* 💰\n"\
                f"══════════════════\n"\
                f"🔘 Поставлено: {user_casino['bid']}\n"\
                f"💳 Доступно: {user['money']}\n"\
                f"══════════════════\n"
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.dice_kb)

@bot.callback_query_handler(lambda call: call.data == 'roll_dice')
def roll_dice(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_casino = db.get_casino(id)
    numbers = gl.dice_random()
    numbers_diller = numbers[0]
    numbers_user = numbers[1]
    photo = open(f'image/dice/{numbers_diller[0]}_{numbers_diller[1]}_{numbers_user[0]}_{numbers_user[1]}.png', 'rb')

    if user['money'] < user_casino['bid'] or user['money'] < 10:
        text = f"😢 Упс! Не хватает монет..."
        bot.edit_message_caption(text, id, call.message.message_id, reply_markup=kb.back_casino_kb)
        return

    if numbers_diller[0] + numbers_diller[1] > numbers_user[0] + numbers_user[1]:
        db.edit_money(id, user_casino['bid'])
        user = db.get_me(id)
        text = f"Д: {numbers_diller[0] + numbers_diller[1]} | Ты: {numbers_user[0] + numbers_user[1]}\n" \
                f"✖ Проигрыш: -{user_casino['bid']}\n" \
                f"💰 Баланс: {user['money']}"
    elif numbers_diller[0] + numbers_diller[1] < numbers_user[0] + numbers_user[1]:
        db.add_money(id, user_casino['bid'])
        user = db.get_me(id)
        text = f"Д: {numbers_diller[0] + numbers_diller[1]} | Ты: {numbers_user[0] + numbers_user[1]}\n" \
                f"✔ Выигрыш: +{user_casino['bid']}\n" \
                f"💰 Баланс: {user['money']}"
    else:
        text = f"Д: {numbers_diller[0] + numbers_diller[1]} | Ты: {numbers_user[0] + numbers_user[1]}\n" \
                f"➖ Ничья\n" \
                f"💰 Баланс: {user['money']}"
    bot.delete_message(id, call.message.message_id)
    bot.send_photo(id, photo, text, reply_markup=kb.back_dice_kb)
    


def post_listing(id, item_id, price, quantity):
    db = Database()
    post_id = db.set_product(id, item_id, price, quantity, gl.end_time(growth_hours=24))
    item_info = db.get_items_id(item_id)
    text = f"🛒 *Новый товар!* #{post_id}\n\n"\
            f"*Товар:* {item_info['name']}\n"\
            f"*Количество:* {quantity}\n"\
            f"*Цена:* {price} монет"
    mesg = bot.send_message(ID_CHANNEL_MARKET, text, reply_markup=kb.product(post_id))
    db.set_message_id_product(post_id, mesg.message_id)

@bot.message_handler(commands=['sell'])
def handle_sell(message):
    id = message.from_user.id
    db = Database()
    user = db.get_me(id)

    if user['locate'] == 'training':
        bot.send_message(id, 
                         "⛔ Пожалуйста, используйте кнопки для прохождения обучения. Вы не можете использовать другие команды сейчас.", 
                         reply_markup=kb.continue_training_kb)
        return
    
    user_market = db.get_products_user(id)
    if len(user_market) == user['max_product']:
        bot.send_message(id, 'У тебя нет свободных слотов', reply_markup=kb.back_main_menu_kb)
        return
    args = message.text.split()[1:]
    if len(args) < 3:
        bot.send_message(id, "Использование: /sell [id товара] [количество] [цена]\n"\
                                "Цена ставится за общее количетсво товара", reply_markup=kb.back_main_menu_kb)
        return
    item_id, quantity, price = args[0], args[1], args[2]
    try:
        item_id = int(item_id)
        quantity = int(quantity)
        price = int(price)
        if item_id not in ID_ITEM_FOR_SELL:
            bot.send_message(id, 'Товар нельзя продать', reply_markup=kb.back_main_menu_kb)
            return
        user_inventory_item = db.get_item_invetory(id, item_id)
        if user_inventory_item != None:
            if user_inventory_item['quantity'] >= quantity:
                post_listing(message.from_user.id, item_id, price, quantity)
                db.remove_item_id(id, item_id, quantity)
                bot.send_message(id, f"✅ Товар {item_id} выставлен на продажу!", reply_markup=kb.back_main_menu_kb)
            else:
                bot.send_message(id, f"У тебя нет такого количества", reply_markup=kb.back_main_menu_kb)
        else:
            bot.send_message(id, f"У тебя нет данного предмета", reply_markup=kb.back_main_menu_kb)
    except ValueError:
        bot.send_message(id, "Ошибка: id товара, количество и цена должны быть числами", reply_markup=kb.back_main_menu_kb)

@bot.callback_query_handler(lambda call: call.data == 'sell')
def sell(call):
    id = call.from_user.id
    text =  f'Использование: /sell [id товара] [количество] [цена]\n'\
            f'Цена ставится за общее количетсво товара'
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_main_menu_kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy(call):
    id = call.from_user.id
    post_id = int(call.data.split('_')[1])
    db = Database()
    user = db.get_me(id)
    post = db.get_product(post_id)
    info_item = db.get_items_id(post['id_item'])

    if not(post):
        bot.answer_callback_query(call.id, "Товар уже продан")
        return
    
    if id == post['id_owner']:
        bot.answer_callback_query(call.id, "Ты не можешь купить свой товар!")
        return
    
    if user['money'] < post['price']:
        bot.answer_callback_query(call.id, 'У тебя нехватает денег')
        return

    db.delete_product(post_id)
    db.edit_money(id, post['price'])
    db.set_inventory(id, post['id_item'], post['quantity'])
    db.add_money(post['id_owner'], post['quantity'])
    bot.delete_message(ID_CHANNEL_MARKET, call.message.message_id)

    bot.send_message(post['id_owner'], 
                     f"У тебя купили {info_item['name']} в количестве {post['quantity']}", reply_markup=kb.back_main_menu_kb)
    
    bot.answer_callback_query(call.id,f"Вы купили {info_item['name']}!")

@bot.callback_query_handler(lambda call: call.data == 'market')
def market(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)
    user_market = db.get_products_user(id)
    if user_market == []:
        text = f'Ты ничего не продаешь\n'\
                f"Свободных лотов: {user['max_product']}\n\n"\
                f'Канал с товарами: @farmhappymarket'
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.market_kb)
    else:
        text = ''
        for item in user_market:
            info_item = db.get_items_id(item['id_item'])
            text += f"≡ {info_item['name']} ≡\n" \
                    f"▪ ID: {item['id']}\n" \
                    f"▪ Кол-во: {item['quantity']}\n" \
                    f"▪ Цена: {item['price']}\n\n"
        text += f"Свободных лотов: {user['max_product'] - len(user_market)}\n\n"\
                f'Канал с товарами: @farmhappymarket'
        bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.market_kb)

@bot.callback_query_handler(lambda call: call.data == 'cancel_sell')
def cancel_sell(call):
    id = call.from_user.id 
    db = Database()
    user_market = db.get_products_user(id)
    if user_market == None:
        bot.answer_callback_query(call.id, 'У тебя нет выставленных товаров на продажу')
        return
    
    text = f'Нажми на слот, который хочешь отменить'
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.cancel_sell(user_market))

@bot.callback_query_handler(lambda call: call.data.startswith('slot_cancel_'))
def slot_cancel(call):
    id = call.from_user.id
    slot_id = int(call.data.split('_')[2])
    db = Database()
    post = db.get_product(slot_id)
    text = f'Товар убран из списка продаж'

    if not(post):
        bot.answer_callback_query(call.id, "Товар уже продан")
        return
    
    db.set_inventory(id, post['id_item'], post['quantity'])
    db.delete_product(slot_id)
    bot.delete_message(ID_CHANNEL_MARKET, post['message_id'])
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_market_kb)



@bot.message_handler(commands=['support'])
def support(message):
    id = message.from_user.id
    db = Database()
    user = db.get_me(id)

    if user['locate'] == 'training':
        bot.send_message(id, 
                         "⛔ Пожалуйста, используйте кнопки для прохождения обучения. Вы не можете использовать другие команды сейчас.", 
                         reply_markup=kb.continue_training_kb)
        return

    text = f'✉️ Чтобы написать о своей(ем) проблеме/вопросе используй команду /report [текст проблемы]'
    bot.send_message(id, text, reply_markup=kb.support_kb)

@bot.callback_query_handler(lambda call: call.data == 'support')
def support(call):
    id = call.from_user.id
    text = f'✉️ Чтобы написать о своей(ем) проблеме/вопросе используй команду /report [текст проблемы]'
    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.support_kb)

@bot.message_handler(commands=['report'])
def report(message):
    '''
    /report [text]
    '''

    id = message.from_user.id
    db = Database()
    user = db.get_me(id)
    user_reports = db.get_report_addressing(id)

    if user['locate'] == 'training':
        bot.send_message(id, 
                         "⛔ Пожалуйста, используйте кнопки для прохождения обучения. Вы не можете использовать другие команды сейчас.", 
                         reply_markup=kb.continue_training_kb)
        return

    if len(user_reports) == 3: 
        bot.send_message(id, "❌ Можно отправить только 3 обращения.") 
        return

    text_report = message.text[8:]

    if text_report == '':
        text = f'✉️ Чтобы написать о своей(ем) проблеме/вопросе используй команду /report [текст проблемы]'
        bot.send_message(id, text, reply_markup=kb.back_main_menu_kb)
        return
    

    id_report = db.set_report(id, text_report)
    
    info_report = db.get_report(id_report)

    text_for_support = f'Новое обращение №{id_report}\n\n'\
                        f"ID игрока: {info_report['id_addressing']}\n"\
                        f'Текст: {text_report}'

    text = f'✅ Обращение получено'
    bot.send_message(id, text, reply_markup=kb.back_main_menu_kb)
    bot.send_message(ID_CHAT_REPORTS, text_for_support)


@bot.message_handler(commands=['reply_report'])
def reply_report(message):
    '''
    /reply_report [id_report] [state] [text]
    '''
    if message.chat.type == 'group':
        id_supported = message.from_user.id
        db = Database()
        text = message.text[14:]
        args = message.text.split(maxsplit=3)[1:]
        if text == '' or len(args) < 3:
            bot.reply_to(message, 'Команда /reply_report [ID обращения] [состояние обращения] [текст]')
            return
        
        id_report, state, text_reply_report = args[0], args[1], args[2]
        try:
            id_report = int(id_report)
            state = int(state)
            info_report = db.get_report(id_report)

            if state == 1:
                text_for_addressing = f'Ответ на обращение: \n'\
                                        f'{text_reply_report}\n\n'\
                                        f'Чтобы продолжить диалог используй:\n'\
                                        f'/report_id [ID обращения] [текст]'
            elif state == 2:
                text_for_addressing = f'Ответ на обращение: \n'\
                                        f'{text_reply_report}\n\n'\
                                        f'Решение: Отказано в обращение'
            elif state == 3:
                text_for_addressing = f'Ответ на обращение: \n'\
                                        f'{text_reply_report}\n\n'\
                                        f'Решение: Решено'
            else:
                bot.reply_to(message, 'Введено неверное состояние!')
                return

            db.update_state_report(id_report, state, id_supported)

            bot.send_message(info_report['id_addressing'], text_for_addressing)
            bot.reply_to(message, '✅ Удачно')
        except ValueError:
            bot.reply_to(message, 'Ошибка: ID обращения и состояние должны быть целыми числами')
        

@bot.message_handler(commands=['report_id'])
def report_id(message):
    '''
    /report_id [id_report] [text]
    '''
    id = message.from_user.id
    db = Database()
    user = db.get_me(id)
    
    if user['locate'] == 'training':
        bot.send_message(id, 
                         "⛔ Пожалуйста, используйте кнопки для прохождения обучения. Вы не можете использовать другие команды сейчас.", 
                         reply_markup=kb.continue_training_kb)
        return
    
    args = message.text.split(maxsplit=2)[1:]
    id_report, text = args[0], args[1]
    try:
        id_report = int(id_report)
        info_report = db.get_report(id_report)

        if info_report == None or info_report['id_addressing'] != id:
            bot.send_message(id, 'Такого обращения нет', reply_markup=kb.back_main_menu_kb)
            return
        
        bot.send_message(id, '✅ Удачно', reply_markup=kb.back_main_menu_kb)

        text_for_support = f'Обновление обращения №{id_report}\n\n'\
                            f'{text}'
        bot.send_message(ID_CHAT_REPORTS, text_for_support)

    except ValueError:
        bot.send_message(id, 'ID обращения должно быть цклым числом', reply_markup=kb.back_main_menu_kb)

@bot.callback_query_handler(lambda call: call.data == 'my_reports')
def my_reports(call):
    id = call.from_user.id
    db = Database()
    reports = db.get_report_addressing(id)
    text = f"📋 <b>Твои активные обращения:</b>\n\n"
    for report in reports:
        text += f"🆔 <b>ID:</b> {report['id']}\n"
        if report['state'] == 0:
            text += f"🟢 <b>Состояние:</b> Новое обращение 🆕\n"
        else:
            text += f"🟡 <b>Состояние:</b> В процессе решения 🔄\n"
        text += f"📝 <b>Текст обращения:</b>\n"\
                f"┗ <i>{report['text']}</i>\n"\
                f"────────────────────\n\n"

    bot.edit_message_text(text, id, call.message.message_id, reply_markup=kb.back_support_kb, parse_mode='html')


@bot.message_handler(commands=['daily_bonus'])
def daily_bonus(message):
    id = message.from_user.id
    db = Database()
    user = db.get_me(id)

    if user['locate'] == 'training':
        bot.send_message(id, 
                         "⛔ Пожалуйста, используйте кнопки для прохождения обучения. Вы не можете использовать другие команды сейчас.", 
                         reply_markup=kb.continue_training_kb)
        return

    if user['daily_bonus'] == 0:
        text = f"🎁 <b>Ежедневный бонус</b> 🎁\n\n"\
               f"Сегодня ты можешь получить:\n"\
               f"💰 <i>Монеты</i>\n"\
               f"📦 <i>Рандомный бокс</i>\n"\
               f"🌱 <i>Семена</i>\n\n"\
               f"📌 <b>Условие:</b> нужно быть подписанным на канал\n"\
               f"🌐 <b>Новостной паблик Happy Farm:</b> @newsHappyFarm\n\n"\
               f"🔹 После подписки нажми кнопку <b>'Проверить подписку'</b>"
        bot.send_message(id, text, reply_markup=kb.check_follow_kb, parse_mode='HTML')
    else:
        text = f"⏳ <b>Бонус уже получен!</b>\n\n"\
               f"Ты сегодня уже забирал свой подарок.\n"\
               f"🕒 Приходи завтра за новым бонусом!"
        bot.send_message(id, text, parse_mode='HTML')

@bot.callback_query_handler(lambda call: call.data == 'daily_bonus')
def daily_bonus_call(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)

    if user['daily_bonus'] == 0:
        text = f"🎁 <b>Ежедневный бонус</b> 🎁\n\n"\
               f"Сегодня ты можешь получить:\n"\
               f"💰 <i>Монеты</i>\n"\
               f"📦 <i>Рандомный бокс</i>\n"\
               f"🌱 <i>Семена</i>\n\n"\
               f"📌 <b>Условие:</b> нужно быть подписанным на канал\n"\
               f"🌐 <b>Новостной паблик Happy Farm:</b> @newsHappyFarm\n\n"\
               f"🔹 После подписки нажми кнопку <b>'Проверить подписку'</b>"
        bot.edit_message_text(text, id, call.message.message_id, 
                            reply_markup=kb.check_follow_kb, parse_mode='HTML')
    else:
        text = f"⏳ <b>Бонус уже получен!</b>\n\n"\
               f"Ты сегодня уже забирал свой подарок.\n"\
               f"🕒 Приходи завтра за новым бонусом!"
        bot.edit_message_text(text, id, call.message.message_id, parse_mode='HTML')

@bot.callback_query_handler(lambda call: call.data == 'check_follow')
def check_follow(call):
    id = call.from_user.id
    try:
        member = bot.get_chat_member(ID_CHANNEL_NEWS, id)
        if member.status in ['member', 'administrator', 'creator']:
            bot.edit_message_reply_markup(id, call.message.message_id, 
                                        reply_markup=kb.get_daily_bonus_kb)
            bot.answer_callback_query(call.id, "✅ Подписка подтверждена! Можешь забирать бонус")
        else:
            bot.answer_callback_query(call.id, '❌ Ты не подписан на канал!', show_alert=True)
    except Exception as e:
        bot.answer_callback_query(call.id, f'⚠️ Ошибка: {e}', show_alert=True)

@bot.callback_query_handler(lambda call: call.data == 'get_daily_bonus')
def get_daily_bonus(call):
    id = call.from_user.id
    db = Database()
    user = db.get_me(id)

    if user['daily_bonus'] == 1:
        text = f"⏳ Ты уже забирал сегодняшний бонус!"
        bot.delete_message(id, call.message.message_id)
        bot.answer_callback_query(call.id, text, show_alert=True)
        return
    
    reward = gl.generate_random_daily_bonus()
    info_item = db.get_items_id(reward[0])

    text = f"🎉 <b>Поздравляем с получением бонуса!</b> 🎉\n\n"\
           f"Ты получил:\n"\
           f"🎁 <b>{info_item['name']}</b> x{reward[1]}\n\n"\
           f"🕒 Следующий бонус будет доступен завтра!"
           
    bot.edit_message_text(text, id, call.message.message_id, parse_mode='HTML')
    if reward[0] == 0:
        db.add_money(id, reward[1])
    else:
        db.set_inventory(id, reward[0], reward[1])
    db.set_daily_bonus(id, 1)

    



# Временные функции 

def update_tasks():
    db = Database()
    users = db.get_all_id_users()
    for user in users:
        info_of_user = db.get_info_for_tasks(user['id'])
        db.set_tasks(user['id'], gl.generate_tasks(info_of_user))

def send_notification_harvest():
    db = Database()
    users = db.get_id_users_ready_harvest()
    for user in users:
        if gl.check_time(user['time_end']):
            bot.send_message(user['id_owner'], f"На грядке №{user['id_bed']} вырос урожай")
            db.set_state_bed(user['id_owner'], user['id_bed'], 2)

def daily_bonus_reset():
    db = Database()
    db.reset_daily_bonus()

def delete_post_market():
    db = Database()
    products = db.get_all_product()
    for product in products:
        if gl.check_time(product['time_delete']):
            db.set_inventory(product['id_owner'], product['id_item'], product['quantity'])
            db.delete_product(product['id'])
            bot.delete_message(ID_CHANNEL_MARKET, product['message_id'])
            text = f"🛒 Товар #{product['id']} снят с торговой площадки.\n"\
                    f"🔙 Все предметы были перемещены обратно в инвентарь."
            bot.send_message(product['id_owner'], text)
    


schedule.every(1).minutes.do(send_notification_harvest)
schedule.every().day.at('00:00').do(update_tasks)
schedule.every().day.at('00:00').do(daily_bonus_reset)
schedule.every(1).minutes.do(delete_post_market)



def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


scheduler_thread = threading.Thread(target=scheduler, daemon=True).start()

bot.polling(none_stop=True, interval=0)