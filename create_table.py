import sqlite3

def create_database(database_name='users.db'):
    # Подключение к базе данных (файл будет создан, если его нет)
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Создание таблиц
    cursor.executescript("""
    PRAGMA foreign_keys = off;
    BEGIN TRANSACTION;

    -- Таблица: bed
    CREATE TABLE IF NOT EXISTS bed (
        id_bed INTEGER, 
        id_owner INTEGER, 
        state INTEGER, 
        watering INTEGER, 
        id_planted INTEGER REFERENCES items (item_id), 
        time_end_watering INTEGER, 
        time_end INTEGER, 
        holes INTEGER, 
        chance_resistance INTEGER, 
        resistance INTEGER, 
        watering_hours INTEGER, 
        up_speed_rate INTEGER, 
        last_price_added_holes INTEGER
    );

    -- Таблица: casino
    CREATE TABLE IF NOT EXISTS casino (
        id INTEGER, 
        bid INTEGER
    );

    -- Таблица: farm
    CREATE TABLE IF NOT EXISTS farm (
        id INTEGER PRIMARY KEY ON CONFLICT IGNORE, 
        amount_beds INTEGER, 
        buster INTEGER
    );

    -- Таблица: inventory
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER, 
        item_id INTEGER REFERENCES items (item_id), 
        quantity INTEGER
    );

    -- Таблица: items
    CREATE TABLE IF NOT EXISTS items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        price INTEGER, 
        sell_price INTEGER, 
        strength INTEGER, 
        type TEXT
    );

    -- Таблица: market
    CREATE TABLE IF NOT EXISTS market (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        id_owner INTEGER, 
        id_item INTEGER, 
        price INTEGER, 
        quantity INTEGER, 
        message_id INTEGER
    );

    -- Таблица: reports
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        id_addressing INTEGER, 
        text TEXT, 
        state INTEGER, 
        id_supported INTEGER
    );

    -- Таблица: tasks
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER, 
        text_task1 TEXT, 
        task1 INTEGER, 
        plant1 INTEGER, 
        task1_completed INTEGER, 
        text_task2 TEXT, 
        task2 INTEGER, 
        plant2 INTEGER, 
        task2_completed INTEGER, 
        get_reward INTEGER
    );

    -- Таблица: tool
    CREATE TABLE IF NOT EXISTS tool (
        id INTEGER, 
        tool_id INTEGER REFERENCES items (item_id), 
        strength INTEGER
    );

    -- Таблица: user
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY ON CONFLICT IGNORE, 
        money INTEGER, 
        locate TEXT, 
        gold_money INTEGER, 
        max_product INTEGER, 
        message_id_bot INTEGER, 
        buster_x10_time_all INTEGER
    );

    COMMIT TRANSACTION;
    PRAGMA foreign_keys = on;
    """)

    # Вставка начальных данных в таблицу items
    items_data = [
        (0, None, None, None, None, None),
        (1, 'Пшеница (семена)', 10, None, None, 'семена'),
        (2, 'Морковь (семена)', 20, None, None, 'семена'),
        (3, 'Кукуруза (семена)', 25, None, None, 'семена'),
        (4, 'Картофель (семена)', 50, None, None, 'семена'),
        (5, 'Лунный лотос (семена)', 500, None, None, 'семена'),
        (6, 'Огненный перец (семена)', 300, None, None, 'семена'),
        (7, 'Деревянные грабли', 100, None, 50, 'грабли'),
        (8, 'Стальные грабли', 500, None, 100, 'грабли'),
        (9, 'Железные грабли', 200, None, 150, 'грабли'),
        (10, 'Грабли дождя', 3000, None, 15, 'грабли'),
        (11, 'Грабли Сновидений', 1500, None, 150, 'грабли'),
        (12, 'Квантовые грабли', 2500, None, 200, 'грабли'),
        (13, 'Молекула дождя', None, None, None, 'ресурс'),
        (14, 'Сновиденческая трава', None, None, None, 'ресурс'),
        (15, 'Квантовый обломок', None, None, None, 'ресурс'),
        (16, 'Пшеница (урожай)', None, 15, None, 'урожай'),
        (17, 'Морковь (урожай)', None, 30, None, 'урожай'),
        (18, 'Кукуруза (урожай)', None, 40, None, 'урожай'),
        (19, 'Картофель (урожай)', None, 80, None, 'урожай'),
        (20, 'Лунный лотос (урожай)', None, 800, None, 'урожай'),
        (21, 'Огненный перец (урожай)', None, 450, None, 'урожай'),
        (22, 'Лечебная трава', None, None, None, 'ресурс'),
        (23, 'Обычный бокс', None, None, None, 'бокс'),
        (24, 'Редкий бокс', None, None, None, 'бокс'),
        (25, 'Эпический бокс', None, None, None, 'бокс'),
        (26, 'Легендарный бокс', None, None, None, 'бокс'),
        (27, 'Бустер "Отказ от воды"', None, None, None, 'бустер'),
        (28, 'Бустер "Удвоенный урожай"', None, None, None, 'бустер'),
        (29, 'Бустер "Отсутствие болезней"', None, None, None, 'бустер')
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO items (item_id, name, price, sell_price, strength, type) 
    VALUES (?, ?, ?, ?, ?, ?)
    """, items_data)

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()
