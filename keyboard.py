from telebot import types

profile_kb = types.InlineKeyboardMarkup()
profile_kb.add(
    types.InlineKeyboardButton('🏰 Кланы', callback_data='clans'),
    types.InlineKeyboardButton('📜 Задания', callback_data='tasks'),
    types.InlineKeyboardButton('💎 Донат', callback_data='donate'),
)

back_profile_kb = types.InlineKeyboardMarkup()
back_profile_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='profile'))

city_kb = types.InlineKeyboardMarkup()
city_kb.add(
    types.InlineKeyboardButton('🛍️ Магазин', callback_data='shop'),
    types.InlineKeyboardButton('🏪 Рынок', callback_data='market'),
    types.InlineKeyboardButton('🎰 Казино', callback_data='casino'),
    types.InlineKeyboardButton('💰 Скупщик', callback_data='buyer'),
    
)

shop_kb = types.InlineKeyboardMarkup(row_width=2)
shop_kb.add(
    types.InlineKeyboardButton('🌱 Семена', callback_data='seeds'),
    types.InlineKeyboardButton('🛠️ Грабли', callback_data='rakes'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='city')
)

seeds_kb = types.InlineKeyboardMarkup()
seeds_kb.add(types.InlineKeyboardButton('🌾 Пшеница (семена)', callback_data='buy_seeds_wheat'))
seeds_kb.add(types.InlineKeyboardButton('🥕 Морковь (семена)', callback_data='buy_seeds_carrot'))
seeds_kb.add(types.InlineKeyboardButton('🌽 Кукуруза (семена)', callback_data='buy_seeds_corn'))
seeds_kb.add(types.InlineKeyboardButton('🥔 Картофель (семена)', callback_data='buy_seeds_potato'))
seeds_kb.add(
    types.InlineKeyboardButton('1/2', callback_data='q'),
    types.InlineKeyboardButton('➡️', callback_data='seeds_2')
)
seeds_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='shop'))

seeds_2_kb = types.InlineKeyboardMarkup()
seeds_2_kb.add(types.InlineKeyboardButton('🌶️ Огненный перец (семена)', callback_data='buy_seeds_fire_pepper'))
seeds_2_kb.add(types.InlineKeyboardButton('🌸 Лунный лотос (семена)', callback_data='buy_seeds_moon_lotus'))
seeds_2_kb.add(
    types.InlineKeyboardButton('⬅️', callback_data='seeds'),
    types.InlineKeyboardButton('2/2', callback_data='q')
)
seeds_2_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='shop'))

card_seeds_kb = types.InlineKeyboardMarkup()
card_seeds_kb.add(
    types.InlineKeyboardButton('1️⃣', callback_data='quantity_buy_1'),
    types.InlineKeyboardButton('5️⃣', callback_data='quantity_buy_5'),
    types.InlineKeyboardButton('🔟', callback_data='quantity_buy_10'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='seeds')
)

rakes_kb = types.InlineKeyboardMarkup()
rakes_kb.add(types.InlineKeyboardButton('🪵 Деревянные грабли', callback_data='buy_rake_wood'))
rakes_kb.add(types.InlineKeyboardButton('🛠️ Железные грабли', callback_data='buy_rake_iron'))
rakes_kb.add(types.InlineKeyboardButton('⚙️ Стальные грабли', callback_data='buy_rake_steel'))
rakes_kb.add(
    types.InlineKeyboardButton('1/2', callback_data='q'),
    types.InlineKeyboardButton('➡️', callback_data='rakes_2')
)
rakes_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='shop'))

rakes_2_kb = types.InlineKeyboardMarkup()
rakes_2_kb.add(types.InlineKeyboardButton('🌧️ Грабли дождя', callback_data='buy_rake_rain'))
rakes_2_kb.add(types.InlineKeyboardButton('💤 Грабли Сновидений', callback_data='buy_rake_dreams'))
rakes_2_kb.add(types.InlineKeyboardButton('⚛️ Квантовые грабли', callback_data='buy_rake_quantum'))
rakes_2_kb.add(
    types.InlineKeyboardButton('⬅️', callback_data='rakes'),
    types.InlineKeyboardButton('2/2', callback_data='q')
)
rakes_2_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='shop'))

card_rakes_kb = types.InlineKeyboardMarkup()
card_rakes_kb.add(
    types.InlineKeyboardButton('🛒 Купить', callback_data='buy_rakes'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='rakes')
)

replace_rakes_kb = types.InlineKeyboardMarkup()
replace_rakes_kb.add(
    types.InlineKeyboardButton('✅', callback_data='replace_rake'),
    types.InlineKeyboardButton('❌', callback_data='rakes')
)

def make_beds(amount_beds):
    beds_kb = types.InlineKeyboardMarkup()
    if amount_beds > 4:
        for bed in range(1, 5):
            beds_kb.add(types.InlineKeyboardButton(f'🛏️ Грядка №{bed}', callback_data=f'bed_{bed}'))
        beds_kb.add(
            types.InlineKeyboardButton('1/2', callback_data='q'),
            types.InlineKeyboardButton('➡️', callback_data='beds_2')
        )
        beds_2_kb = types.InlineKeyboardMarkup()
        for bed in range(5, amount_beds+1):
            beds_2_kb.add(types.InlineKeyboardButton(f'🌿 Грядка №{bed}', callback_data=f'bed_{bed}'))
        beds_2_kb.add(
            types.InlineKeyboardButton('⬅️', callback_data='beds'),
            types.InlineKeyboardButton('2/2', callback_data='q')
        )
        if amount_beds < 10:
            beds_2_kb.add(
                types.InlineKeyboardButton('🛒 Купить грядку', callback_data='buy_bed'),
                types.InlineKeyboardButton('⚡ Бустеры', callback_data='busters')
            )
        else:
            beds_2_kb.add(types.InlineKeyboardButton('⚡ Бустеры', callback_data='busters'))
        return [beds_kb, beds_2_kb]
    else:
        for bed in range(1, amount_beds+1):
            beds_kb.add(types.InlineKeyboardButton(f'🌿 Грядка №{bed}', callback_data=f'bed_{bed}'))
        beds_kb.add(
            types.InlineKeyboardButton('🛒 Купить грядку', callback_data='buy_bed'),
            types.InlineKeyboardButton('⚡ Бустеры', callback_data='busters')
        )
        return [beds_kb]

buy_beds_kb = types.InlineKeyboardMarkup()
buy_beds_kb.add(
    types.InlineKeyboardButton('🛒 Купить грядку', callback_data='buy_new_bed'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='beds')
)

bed_state_0_kb = types.InlineKeyboardMarkup(row_width=1)
bed_state_0_kb.add(
    types.InlineKeyboardButton('🌱 Посадить семена', callback_data='set_seeds'),
    types.InlineKeyboardButton('⚙️ Улучшения', callback_data='upgrade_bed'),
    types.InlineKeyboardButton('💦 Полить', callback_data='watering'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='beds')
)

def bed_state_1(time):
    bed_state_1_kb = types.InlineKeyboardMarkup(row_width=1)
    bed_state_1_kb.add(
        types.InlineKeyboardButton(f'⏳ {time[0]}', callback_data=f'{time[1]}'),
        types.InlineKeyboardButton('⚙️ Улучшения', callback_data='upgrade_bed'),
        types.InlineKeyboardButton('💦 Полить', callback_data='watering'),
        types.InlineKeyboardButton('🔙 Назад', callback_data='beds')
    )
    return bed_state_1_kb

bed_state_2_kb = types.InlineKeyboardMarkup(row_width=1)
bed_state_2_kb.add(
    types.InlineKeyboardButton('🔄 Собрать урожай', callback_data='get_harvest'),
    types.InlineKeyboardButton('⚙️ Улучшения', callback_data='upgrade_bed'),
    types.InlineKeyboardButton('💦 Полить', callback_data='watering'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='beds')
)

def select_set_seeds(inventory_items, call_data):
    select_set_seeds_kb = types.InlineKeyboardMarkup(row_width=1)
    for item in inventory_items:
        select_set_seeds_kb.add(
            types.InlineKeyboardButton(f"🌱 {item['name']} - {item['quantity']} шт", callback_data=f"set_seeds_{item['item_id']}")
        )
    select_set_seeds_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data=call_data))
    return select_set_seeds_kb

back_beds = types.InlineKeyboardMarkup()
back_beds.add(types.InlineKeyboardButton('🔙 Назад', callback_data='beds'))

back_select_set_seeds = types.InlineKeyboardMarkup()
back_select_set_seeds.add(types.InlineKeyboardButton('🔙 Назад', callback_data='set_seeds'))

def back_get_harvest(call_data):
    back_get_harvest_kb = types.InlineKeyboardMarkup()
    back_get_harvest_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data=call_data))
    return back_get_harvest_kb

def upgrade_bed(call_data):
    upgrade_bed_kb = types.InlineKeyboardMarkup(row_width=1)
    upgrade_bed_kb.add(
        types.InlineKeyboardButton('💊 Устойчивость к заболеваниям', callback_data='disease_resistance'),
        types.InlineKeyboardButton('🌧️ Уменьшение жажды почвы', callback_data='reducing_soil'),
        types.InlineKeyboardButton('🕳️ Увеличить количество лунок', callback_data='up_number_holes'),
        types.InlineKeyboardButton('🔙 Назад', callback_data=call_data)
    )
    return upgrade_bed_kb

disease_resistance_kb = types.InlineKeyboardMarkup(row_width=2)
disease_resistance_kb.add(
    types.InlineKeyboardButton('🔼 Улучшить', callback_data='upgrade_disease_resistance'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='upgrade_bed')
)

back_to_upgrade_kb = types.InlineKeyboardMarkup()
back_to_upgrade_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='upgrade_bed'))

reducing_soil_kb = types.InlineKeyboardMarkup(row_width=2)
reducing_soil_kb.add(
    types.InlineKeyboardButton('🔼 Улучшить', callback_data='upgrade_reducing_soil'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='upgrade_bed')
)

added_holes_kb = types.InlineKeyboardMarkup(row_width=2)
added_holes_kb.add(
    types.InlineKeyboardButton('🔼 Улучшить', callback_data='added_holes'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='upgrade_bed')
)

def buyer(inventory_user):
    buyer_kb = types.InlineKeyboardMarkup()
    for item in inventory_user:
        buyer_kb.add(
            types.InlineKeyboardButton(f"💰 {item['name']} - {item['quantity']}", callback_data=f"sell_item_{item['item_id']}")
        )
    buyer_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='city'))
    return buyer_kb

back_buyer_kb = types.InlineKeyboardMarkup()
back_buyer_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='buyer'))

get_reward_kb = types.InlineKeyboardMarkup(row_width=1)
get_reward_kb.add(
    types.InlineKeyboardButton('🎁 Получить награду', callback_data='get_reward'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='profile')
)

back_tasks_kb = types.InlineKeyboardMarkup()
back_tasks_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='tasks'))

box_kb = types.InlineKeyboardMarkup()
box_kb.add(
    types.InlineKeyboardButton('🎁 Открыть бокс', callback_data='box'),
    
)

def open_box(user_inventory):
    open_box_kb = types.InlineKeyboardMarkup(row_width=1)
    for item in user_inventory:
        open_box_kb.add(types.InlineKeyboardButton(f"🎁 {item['name']} - {item['quantity']}", callback_data=f"box_{item['item_id']}"))
    open_box_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='inventory'))
    return open_box_kb

open_box_kb = types.InlineKeyboardMarkup(row_width=1)
open_box_kb.add(
    types.InlineKeyboardButton('🎁 Открыть', callback_data='open_box'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='box')
)

back_box_kb = types.InlineKeyboardMarkup()
back_box_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='box'))

def busters(user_data):
    busters_kb = types.InlineKeyboardMarkup(row_width=1)
    for item in user_data:
        busters_kb.add(types.InlineKeyboardButton(f"⚡ {item['name']} - {item['quantity']}", callback_data=f"buster_{item['item_id']}"))
    busters_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='farm'))
    return busters_kb

used_buster_kb = types.InlineKeyboardMarkup(row_width=1)
used_buster_kb.add(
    types.InlineKeyboardButton('⚡ Использовать', callback_data='used_buster'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='busters')
)

back_busters_kb = types.InlineKeyboardMarkup()
back_busters_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='busters'))

casino_kb = types.InlineKeyboardMarkup()
casino_kb.add(
    types.InlineKeyboardButton('🎡 Рулетка', callback_data='roulette'),
    types.InlineKeyboardButton('🎲 Кости', callback_data='dice'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='city')
)

roulette_kb = types.InlineKeyboardMarkup()
roulette_kb.add(
    types.InlineKeyboardButton('1️⃣-1️⃣2️⃣', callback_data='bid_1_12'),
    types.InlineKeyboardButton('1️⃣3️⃣-2️⃣4️⃣', callback_data='bid_13_24'),
    types.InlineKeyboardButton('2️⃣5️⃣-3️⃣6️⃣', callback_data='bid_25_36')
)
roulette_kb.add(
    types.InlineKeyboardButton('⚫ Черный', callback_data='bid_black'),
    types.InlineKeyboardButton('🔴 Красный', callback_data='bid_red')
)
roulette_kb.add(
    types.InlineKeyboardButton('🔢 Чётное', callback_data='bid_even'),
    types.InlineKeyboardButton('0️⃣ Ноль', callback_data='bid_zero'),
    types.InlineKeyboardButton('🔢 Нечётное', callback_data='bid_odd')
)
roulette_kb.add(
    types.InlineKeyboardButton('➗2', callback_data='bid_user_d2'),
    types.InlineKeyboardButton('✖️2', callback_data='bid_user_x2'),
)
roulette_kb.add(
    types.InlineKeyboardButton('➗10', callback_data='bid_user_d10'),
    types.InlineKeyboardButton('✖️10', callback_data='bid_user_x10')
)
roulette_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='casino_back'))

back_casino_kb = types.InlineKeyboardMarkup()
back_casino_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='casino_back'))

dice_kb = types.InlineKeyboardMarkup()
dice_kb.add(
    types.InlineKeyboardButton('🎲 Кинуть кости', callback_data='roll_dice'),
)
dice_kb.add(
    types.InlineKeyboardButton('➗2', callback_data='bid_user_dice_d2'),
    types.InlineKeyboardButton('✖️2', callback_data='bid_user_dice_x2'),
)
dice_kb.add(
    types.InlineKeyboardButton('➗10', callback_data='bid_user_dice_d10'),
    types.InlineKeyboardButton('✖️10', callback_data='bid_user_dice_x10')
)
dice_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='casino'))

back_dice_kb = types.InlineKeyboardMarkup()
back_dice_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='dice_back'))

def product(post_id):
    product_kb = types.InlineKeyboardMarkup()
    product_kb.add(types.InlineKeyboardButton("🛍️ Купить", callback_data=f"buy_{post_id}"))
    return product_kb

market_kb = types.InlineKeyboardMarkup(row_width=2)
market_kb.add(
    types.InlineKeyboardButton('📦 Выставить товар', callback_data='sell'),
    types.InlineKeyboardButton('❌ Отменить товар', callback_data='cancel_sell'),
    types.InlineKeyboardButton('🔙 Назад', callback_data='city')
)

def cancel_sell(user_slots):
    cancel_sell_kb = types.InlineKeyboardMarkup()
    for slot in user_slots:
        cancel_sell_kb.add(types.InlineKeyboardButton(f"📦 Товар №{slot['id']}", callback_data=f"slot_cancel_{slot['id']}"))
    cancel_sell_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='market'))
    return cancel_sell_kb

back_market_kb = types.InlineKeyboardMarkup()
back_market_kb.add(
    types.InlineKeyboardButton('🔙 Назад', callback_data='market')
)

support_kb = types.InlineKeyboardMarkup()
support_kb.add(
    types.InlineKeyboardButton('📢 Мои обращения', callback_data='my_reports')
)

back_support_kb = types.InlineKeyboardMarkup()
back_support_kb.add(types.InlineKeyboardButton('🔙 Назад', callback_data='support'))


back_main_menu_kb = types.InlineKeyboardMarkup()
back_main_menu_kb.add(
    types.InlineKeyboardButton('🏠 На главную', callback_data='profile')
)

start_kb = types.InlineKeyboardMarkup()
start_kb.add(types.InlineKeyboardButton('👣 Пройти обучение', callback_data='pass_training'))

farm_kb = types.InlineKeyboardMarkup()
farm_kb.add(types.InlineKeyboardButton('🦶 Войти на грядку', callback_data='bed_training'))

in_shop_kb = types.InlineKeyboardMarkup()
in_shop_kb.add(types.InlineKeyboardButton('🏪 В магазин', callback_data='in_shop'))

seeds_training_kb = types.InlineKeyboardMarkup()
seeds_training_kb.add(types.InlineKeyboardButton('🌱 Семена', callback_data='seed'))

buy_wheat_kb = types.InlineKeyboardMarkup()
buy_wheat_kb.add(types.InlineKeyboardButton('🌾 Пшеница', callback_data='buy_wheat_training'))

buy_wheat_5_kb = types.InlineKeyboardMarkup()
buy_wheat_5_kb.add(types.InlineKeyboardButton('5️⃣', callback_data='buy_wheat_5'))

rake_kb = types.InlineKeyboardMarkup()
rake_kb.add(types.InlineKeyboardButton('🛠️ Грабли', callback_data='rake_training'))

buy_rake_kb = types.InlineKeyboardMarkup()
buy_rake_kb.add(types.InlineKeyboardButton('🛒 Купить грабли', callback_data='buy_rake_training'))

farm_work_kb = types.InlineKeyboardMarkup()
farm_work_kb.add(types.InlineKeyboardButton('🌱 На ферму', callback_data='farm_work'))

set_seed_kb = types.InlineKeyboardMarkup()
set_seed_kb.add(types.InlineKeyboardButton('🌾 Посадить семена', callback_data='set_seed_training'))

get_harvest_kb = types.InlineKeyboardMarkup()
get_harvest_kb.add(types.InlineKeyboardButton('🧺 Собрать урожай', callback_data='get_harvest_training'))

go_buyer_kb = types.InlineKeyboardMarkup()
go_buyer_kb.add(types.InlineKeyboardButton('🚶 Пошли', callback_data='go_buyer'))

sell_harvest_kb = types.InlineKeyboardMarkup()
sell_harvest_kb.add(types.InlineKeyboardButton('💰 Продать урожай', callback_data='sell_harvest_training'))

go_market_kb = types.InlineKeyboardMarkup()
go_market_kb.add(types.InlineKeyboardButton('🏃 Пошли', callback_data='go_market'))

end_training_kb = types.InlineKeyboardMarkup()
end_training_kb.add(types.InlineKeyboardButton('👌 Понял', callback_data='end_training'))

go_game_kb = types.InlineKeyboardMarkup()
go_game_kb.add(types.InlineKeyboardButton('🎮 Погнали играть!', callback_data='profile'))

continue_training_kb = types.InlineKeyboardMarkup()
continue_training_kb.add(types.InlineKeyboardButton('➡️ Продолжить', callback_data='continue_training'))


check_follow_kb = types.InlineKeyboardMarkup()
check_follow_kb.add(types.InlineKeyboardButton("🔍 Проверить подписку на канал", callback_data='check_follow'))

get_daily_bonus_kb = types.InlineKeyboardMarkup()
get_daily_bonus_kb.add(types.InlineKeyboardButton("🎁 Получить ежедневный бонус", callback_data='get_daily_bonus'))