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
        buster_x10_time_all INTEGER,
        get_harvest_week INTEGER
    );
                         
    -- Таблица: statistics
    CREATE TABLE IF NOT EXISTS statistics (
        new_users_day INTEGER DEFAULT 0,
        new_users_week INTEGER DEFAULT 0
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
        (7, 'Деревянные грабли', 100, None, 20, 'грабли'),
        (8, 'Стальные грабли', 500, None, 40, 'грабли'),
        (9, 'Железные грабли', 200, None, 30, 'грабли'),
        (10, 'Грабли дождя', 3000, None, 50, 'грабли'),
        (11, 'Грабли Сновидений', 1500, None, 50, 'грабли'),
        (12, 'Квантовые грабли', 2500, None, 50, 'грабли'),
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
        (29, 'Бустер "Отсутствие болезней"', None, None, None, 'бустер'),
        (30, 'Случайное семечко', 200, None, None, 'семена')
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO items (item_id, name, price, sell_price, strength, type) 
    VALUES (?, ?, ?, ?, ?, ?)
    """, items_data)

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

def update_database_schema(database_name: str = 'users.db'):
    """
    Обновляет структуру базы данных в соответствии с текущим определением таблиц.
    Если таблицы или колонки отсутствуют, они будут созданы. Если колонки удалены из схемы,
    они будут удалены из таблицы (с предварительным сохранением данных).
    
    Args:
        database_name (str): Имя файла базы данных. По умолчанию 'users.db'.
    """
    # Желаемая структура таблиц из create_table.py
    desired_schema = {
        'bed': [
            ('id_bed', 'INTEGER'), 
            ('id_owner', 'INTEGER'), 
            ('state', 'INTEGER'), 
            ('watering', 'INTEGER'), 
            ('id_planted', 'INTEGER REFERENCES items (item_id)'), 
            ('time_end_watering', 'INTEGER'), 
            ('time_end', 'INTEGER'), 
            ('holes', 'INTEGER'), 
            ('chance_resistance', 'INTEGER'), 
            ('resistance', 'INTEGER'), 
            ('watering_hours', 'INTEGER'), 
            ('up_speed_rate', 'INTEGER'), 
            ('last_price_added_holes', 'INTEGER'),
            ('quantity', 'INTEGER')
        ],
        'casino': [
            ('id', 'INTEGER'), 
            ('bid', 'INTEGER')
        ],
        'farm': [
            ('id', 'INTEGER PRIMARY KEY ON CONFLICT IGNORE'), 
            ('amount_beds', 'INTEGER'), 
            ('buster', 'INTEGER')
        ],
        'inventory': [
            ('id', 'INTEGER'), 
            ('item_id', 'INTEGER REFERENCES items (item_id)'), 
            ('quantity', 'INTEGER')
        ],
        'items': [
            ('item_id', 'INTEGER PRIMARY KEY AUTOINCREMENT'), 
            ('name', 'TEXT'), 
            ('price', 'INTEGER'), 
            ('sell_price', 'INTEGER'), 
            ('strength', 'INTEGER'), 
            ('type', 'TEXT')
        ],
        'market': [
            ('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'), 
            ('id_owner', 'INTEGER'), 
            ('id_item', 'INTEGER'), 
            ('price', 'INTEGER'), 
            ('quantity', 'INTEGER'), 
            ('message_id', 'INTEGER'),
            ('time_delete', 'TEXT')
        ],
        'reports': [
            ('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'), 
            ('id_addressing', 'INTEGER'), 
            ('text', 'TEXT'), 
            ('state', 'INTEGER'), 
            ('id_supported', 'INTEGER')
        ],
        'tasks': [
            ('id', 'INTEGER'), 
            ('text_task1', 'TEXT'), 
            ('task1', 'INTEGER'), 
            ('plant1', 'INTEGER'), 
            ('task1_completed', 'INTEGER'), 
            ('text_task2', 'TEXT'), 
            ('task2', 'INTEGER'), 
            ('plant2', 'INTEGER'), 
            ('task2_completed', 'INTEGER'), 
            ('get_reward', 'INTEGER')
        ],
        'tool': [
            ('id', 'INTEGER'), 
            ('tool_id', 'INTEGER REFERENCES items (item_id)'), 
            ('strength', 'INTEGER')
        ],
        'user': [
            ('id', 'INTEGER PRIMARY KEY ON CONFLICT IGNORE'), 
            ('money', 'INTEGER'), 
            ('locate', 'TEXT'), 
            ('gold_money', 'INTEGER'), 
            ('max_product', 'INTEGER'), 
            ('message_id_bot', 'INTEGER'), 
            ('buster_x10_time_all', 'INTEGER'),
            ('daily_bonus', 'INTEGER DEFAULT 0'),
            ('get_harvest_week', 'INTEGER DEFAULT 0'),
            ('complete_all_goal', 'INTEGER DEFAULT 0')
        ],
        'statistics': {
            ('new_users_day', 'INTEGER DEFAULT 0'),
            ('new_users_week', 'INTEGER DEFAULT 0')
        },
        'events': {
            ('id_event', 'INTEGER'),
            ('goal_complete', 'INTEGER'),
            ('id_planted', 'INTEGER'),
            ('all_goal', 'INTEGER'),
            ('start_time_event', 'TEXT'),
            ('end_time_event', 'TEXT'),
            ('active', 'INTEGER DEFAULT 0')
        }
    }

    # Подключение к базе данных
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    try:
        # Включение поддержки внешних ключей
        cursor.execute("PRAGMA foreign_keys = ON")

        # Получение списка существующих таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]

        # Проверка и обновление каждой таблицы
        for table_name, desired_columns in desired_schema.items():
            if table_name not in existing_tables:
                # Таблица не существует - создаем новую
                columns_sql = ', '.join([f'{col[0]} {col[1]}' for col in desired_columns])
                cursor.execute(f"CREATE TABLE {table_name} ({columns_sql})")
                print(f"Создана таблица: {table_name}")
            else:
                # Таблица существует - проверяем колонки
                cursor.execute(f"PRAGMA table_info({table_name})")
                existing_columns = {row[1]: row[2] for row in cursor.fetchall()}
                
                # Получаем список имен желаемых колонок
                desired_column_names = [col[0] for col in desired_columns]
                
                # 1. Добавляем отсутствующие колонки
                for col_name, col_type in desired_columns:
                    if col_name not in existing_columns:
                        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type}")
                        print(f"Добавлена колонка {col_name} в таблицу {table_name}")
                
                # 2. Удаляем колонки, которых нет в желаемой схеме
                # SQLite не поддерживает DROP COLUMN напрямую, поэтому используем временную таблицу
                columns_to_remove = set(existing_columns.keys()) - set(desired_column_names)
                
                if columns_to_remove:
                    # Создаем временную таблицу с нужной структурой
                    temp_table_name = f"temp_{table_name}"
                    columns_sql = ', '.join([f'{col[0]} {col[1]}' for col in desired_columns])
                    cursor.execute(f"CREATE TABLE {temp_table_name} ({columns_sql})")
                    
                    # Копируем данные из старой таблицы во временную
                    # Выбираем только те колонки, которые есть в обеих таблицах
                    common_columns = set(existing_columns.keys()) & set(desired_column_names)
                    columns_to_select = ', '.join(common_columns)
                    cursor.execute(f"INSERT INTO {temp_table_name} ({columns_to_select}) SELECT {columns_to_select} FROM {table_name}")
                    
                    # Удаляем старую таблицу и переименовываем временную
                    cursor.execute(f"DROP TABLE {table_name}")
                    cursor.execute(f"ALTER TABLE {temp_table_name} RENAME TO {table_name}")
                    
                    print(f"Удалены колонки {', '.join(columns_to_remove)} из таблицы {table_name}")

        # Проверяем начальные данные в таблице items
        cursor.execute("SELECT COUNT(*) FROM items")
        if cursor.fetchone()[0] == 0:
            # Таблица items пустая - вставляем начальные данные
            items_data = [
                # id | name | price | sell_price | strength | type
                (0, None, None, None, None, None),
                (1, 'Пшеница (семена)', 10, None, None, 'семена'),
                (2, 'Морковь (семена)', 20, None, None, 'семена'),
                (3, 'Кукуруза (семена)', 25, None, None, 'семена'),
                (4, 'Картофель (семена)', 50, None, None, 'семена'),
                (5, 'Лунный лотос (семена)', 500, None, None, 'семена'),
                (6, 'Огненный перец (семена)', 300, None, None, 'семена'),
                (7, 'Деревянные грабли', 100, None, 20, 'грабли'),
                (8, 'Стальные грабли', 500, None, 40, 'грабли'),
                (9, 'Железные грабли', 200, None, 30, 'грабли'),
                (10, 'Грабли дождя', 2000, None, 50, 'грабли'),
                (11, 'Грабли Сновидений', 2500, None, 50, 'грабли'),
                (12, 'Квантовые грабли', 2500, None, 50, 'грабли'),
                (13, 'Молекула дождя', None, None, None, 'ресурс'),
                (14, 'Сновиденческая трава', None, None, None, 'ресурс'),
                (15, 'Квантовый обломок', None, None, None, 'ресурс'),
                (16, 'Пшеница (урожай)', None, 15, None, 'урожай'),
                (17, 'Морковь (урожай)', None, 32, None, 'урожай'),
                (18, 'Кукуруза (урожай)', None, 43, None, 'урожай'),
                (19, 'Картофель (урожай)', None, 95, None, 'урожай'),
                (20, 'Лунный лотос (урожай)', None, 1500, None, 'урожай'),
                (21, 'Огненный перец (урожай)', None, 875, None, 'урожай'),
                (22, 'Лечебная трава', None, None, None, 'ресурс'),
                (23, 'Обычный бокс', None, None, None, 'бокс'),
                (24, 'Редкий бокс', None, None, None, 'бокс'),
                (25, 'Эпический бокс', None, None, None, 'бокс'),
                (26, 'Легендарный бокс', None, None, None, 'бокс'),
                (27, 'Бустер "Отказ от воды"', None, None, None, 'бустер'),
                (28, 'Бустер "Удвоенный урожай"', None, None, None, 'бустер'),
                (29, 'Бустер "Отсутствие болезней"', None, None, None, 'бустер'),
                (30, 'Случайное семечко', 425, None, None, 'семена')
            ]
            cursor.executemany("""
            INSERT OR IGNORE INTO items (item_id, name, price, sell_price, strength, type) 
            VALUES (?, ?, ?, ?, ?, ?)
            """, items_data)
            print("Добавлены начальные данные в таблицу items")

        cursor.execute("SELECT COUNT(*) FROM statistics")
        if cursor.fetchone()[0] == 0:
            cursor.execute('INSERT or IGNORE INTO statistics (new_users_day, new_users_week) VALUES (0, 0)')
        conn.commit()
        print("Обновление структуры базы данных завершено успешно")

    except Exception as e:
        conn.rollback()
        print(f"Ошибка при обновлении структуры базы данных: {e}")
        raise
    finally:
        conn.close()
