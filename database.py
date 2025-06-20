import sqlite3
from typing import Optional

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Database:

    _user_id: Optional[int]
    _db: sqlite3.Connection
    _cursor: sqlite3.Cursor

    def __init__(self): # Инициализация БД
        self._db = sqlite3.Connection("users.db", check_same_thread=False)
        self._db.row_factory = dict_factory
        self._cursor = self._db.cursor()


    def get_all_id_users(self):
        self._cursor.execute("SELECT id FROM user")
        return self._cursor.fetchall()


    def check_users(self, id): # Проверка, существует ли пользователь
        self._id = id
        self._cursor.execute("SELECT * FROM user WHERE id = ?", (self._id,))
        user = self._cursor.fetchone()
        if user is None:
            return True # Если нет пользователя
        else:
            return False # Если есть пользователь
        
    def set_user(self, id, buster_time):
        self._id = id
        self._buster_time = buster_time

        self._cursor.execute(
            '''
            INSERT INTO user
            (id, money, locate, gold_money, max_product, message_id_bot, buster_x10_time_all, daily_bonus)
            VALUES
            (?, 400, 'start', 0, 3, 0, ?, 0)
            ''',
            (self._id, self._buster_time, )
        )
        self._db.commit()

    def get_me(self, id):
        self._id = id
        self._cursor.execute(
            '''
            SELECT * FROM user WHERE id = ?
            ''',
            (self._id, )
        )
        return self._cursor.fetchone()
    
    def update_message_id_bot(self, id, message_id):
        self._id = id 
        self._message_id = message_id

        self._cursor.execute(
            '''
            UPDATE user
            SET message_id_bot = ?
            WHERE id = ?
            ''',
            (self._message_id, self._id, )
        )
        self._db.commit()

    def edit_money(self, id, quantity):
        self._id = id
        self._quantity = quantity

        self._cursor.execute(
            '''
            UPDATE user
            SET money = money - ?
            WHERE id = ?
            ''',
            (self._quantity, self._id, )
        )
        self._db.commit()

    def add_money(self, id, quantity):
        self._id = id 
        self._quantity = quantity

        self._cursor.execute(
            '''
            UPDATE user 
            SET money = money + ?
            WHERE id = ?
            ''',
            (self._quantity, self._id, )
        )
        self._db.commit()

    def edit_gold_money(self, id, quantity):
        self._id = id
        self._quantity = quantity

        self._cursor.execute(
            '''
            UPDATE user
            SET gold_money = gold_money - ?
            WHERE id = ?
            ''',
            (self._quantity, self._id, )
        )
        self._db.commit()

    def add_gold_money(self, id, quantity):
        self._id = id 
        self._quantity = quantity

        self._cursor.execute(
            '''
            UPDATE user 
            SET gold_money = gold_money + ?
            WHERE id = ?
            ''',
            (self._quantity, self._id, )
        )
        self._db.commit()

    def edit_locate(self, id, locate):
        self._id = id
        self._locate = locate
        self._cursor.execute(
            '''
            UPDATE user
            SET locate = ?
            WHERE id = ?
            ''',
            (self._locate, self._id, )
        )
        self._db.commit()

    def set_daily_bonus(self, id, state):
        self._id = id
        self._state = state

        self._cursor.execute(
            '''
            UPDATE user
            SET daily_bonus = ?
            WHERE id = ?
            ''',
            (self._state, self._id, )
        )
        self._db.commit()


    def get_inventory(self, id):
        self._id = id
        self._cursor.execute(
            '''
            SELECT items.name, inventory.quantity, items.item_id
            FROM inventory
            JOIN items ON inventory.item_id = items.item_id
            WHERE inventory.id = ?
            ORDER BY inventory.item_id
            ''',
            (self._id, )
        )
        return self._cursor.fetchall()
    
    def get_item_invetory(self, id, item_id):
        self._id = id
        self._item_id = item_id

        self._cursor.execute(
            '''
            SELECT items.name, inventory.quantity
            FROM inventory
            JOIN items ON inventory.item_id = items.item_id
            WHERE inventory.id = ? AND inventory.item_id = ?
            ''',
            (self._id, self._item_id, )
        )
        return self._cursor.fetchone()

    def get_item_inventory_type(self, id, type):
        self._id = id 
        self._type = type

        self._cursor.execute(
            '''
            SELECT inventory.item_id, items.name, items.type, inventory.quantity
            FROM inventory
            JOIN items ON inventory.item_id = items.item_id
            WHERE inventory.id = ? AND items.type = ?
            ORDER BY inventory.item_id
            ''',
            (self._id, self._type, )
        )
        return self._cursor.fetchall()

    def set_inventory(self, id, item_id, quantity = 1):
        self._id = id
        self._item_id = item_id
        self._quantity = quantity
        self._cursor.execute(
            '''
            SELECT quantity FROM inventory 
            WHERE id = ? AND item_id = ?
            ''',
            (self._id, self._item_id)
        )
        result = self._cursor.fetchone()

        if result:
            # Если предмет есть - обновляем количество
            self._new_quantity = result['quantity'] + quantity
            self._cursor.execute(
                '''
                UPDATE inventory 
                SET quantity = ?
                WHERE id = ? AND item_id = ?
                ''',
                (self._new_quantity, self._id, item_id)
            )
        else:
            # Если предмета нет - добавляем новую запись
            self._cursor.execute(
                '''
                INSERT INTO inventory (id, item_id, quantity)
                VALUES (?, ?, ?)
                ''',
                (self._id, self._item_id, self._quantity)
            )
        self._db.commit()
    
    def remove_item_name(self, id, item_name, quantity = 1):
        self._id = id
        self._item_name = item_name
        self._quantity = quantity
        self._cursor.execute('SELECT item_id FROM items WHERE name = ?', (item_name,))
        item_id = self._cursor.fetchone()[0]

        self._cursor.execute(
            '''
            UPDATE inventory
            SET quantity = quantity - ?
            WHERE id = ? AND item_id = ? AND quantity >= ?
            ''',
            (self._quantity, self._id, item_id, self._quantity, )
        )
        self._db.commit()

    def remove_item_id(self, id, item_id, quantity = 1):
        self._id = id
        self._item_id = item_id
        self._quantity = quantity

        self._cursor.execute(
            '''
            UPDATE inventory
            SET quantity = quantity - ?
            WHERE id = ? AND item_id = ? AND quantity >= ?
            ''',
            (self._quantity, self._id, self._item_id, self._quantity, )
        )

        self._cursor.execute('SELECT quantity FROM inventory WHERE id = ? AND item_id = ?',
                             (self._id, self._item_id, ))
        if self._cursor.fetchone()['quantity'] == 0:
            self._cursor.execute(
                '''
                DELETE FROM inventory
                WHERE id = ? AND item_id = ?
                ''',
                (self._id, self._item_id, )
            )

        self._db.commit()

    def set_farm(self, id):
        self._id = id
        self._cursor.execute(
            '''
            INSERT INTO farm
            (id, amount_beds, buster)
            VALUES
            (?, 1, 0)
            ''',
            (self._id, )
        )
        self._db.commit()

    def get_farm(self, id):
        self._id = id
        self._cursor.execute(
            '''
            SELECT *
            FROM farm
            WHERE id = ?
            ''',
            (self._id, )
        )
        return self._cursor.fetchone()

    def used_buster(self, id, buster):
        self._id = id
        self._buster = buster

        self._cursor.execute(
            '''
            UPDATE farm
            SET buster = ?
            WHERE id = ?
            ''',
            (self._buster, self._id, )
        )
        self._db.commit()

    def edit_farm(self, id):
        self._id = id

        self._cursor.execute(
            '''
            UPDATE farm
            SET amount_beds = amount_beds + 1
            WHERE id = ?
            ''',
            (self._id, )
        )
        self._db.commit()

    def set_bed(self, id, id_bed, time_end_watering):
        self._id = id
        self._id_bed = id_bed
        self._time_end_watering = time_end_watering

        self._cursor.execute(
            '''
            INSERT INTO bed
            (id_bed, id_owner, state, watering, id_planted, time_end_watering, 
            time_end, holes, chance_resistance, resistance, watering_hours,
            up_speed_rate, last_price_added_holes)
            VALUES
            (?, ?, 0, 100, 0, ?, 0, 5, 20, 0, 8, 0, 10000)
            ''',
            (self._id_bed, self._id, self._time_end_watering, ),
        )
        self._db.commit()

    def get_bed(self, id, id_bed):
        self._id = id
        self._id_bed = id_bed
        self._cursor.execute(
            '''
            SELECT *
            FROM bed
            JOIN items ON bed.id_planted = items.item_id
            WHERE id_owner = ? AND id_bed = ?
            ''',
            (self._id, self._id_bed, )
        )
        return self._cursor.fetchone()

    def set_state_bed(self, id, id_bed, state):
        self._id = id
        self._state = state
        self._id_bed = id_bed
        self._cursor.execute(
            '''
            UPDATE bed
            SET state = ?
            WHERE id_owner = ? AND id_bed = ?
            ''',
            (self._state, self._id, self._id_bed, )
        )
        self._db.commit()

    def set_seeds_bed(self, id, id_beb, state, id_planted, time_end, resistance):
        self._id = id
        self._id_bed = id_beb
        self._state = state
        self._id_planted = id_planted
        self._time_end = time_end
        self._resistance = resistance

        self._cursor.execute(
            '''
            UPDATE bed
            SET state = ?, id_planted = ?, time_end = ?, resistance = ?
            WHERE id_owner = ? AND id_bed = ?
            ''',
            (self._state, self._id_planted, self._time_end, self._resistance, self._id, self._id_bed, )
        )
        self._db.commit()

    def watering_bed(self, id, id_bed, time_end_watering):
        self._id = id
        self._id_bed = id_bed
        self._time_end_watering = time_end_watering

        self._cursor.execute(
            '''
            UPDATE bed
            SET watering = 100, time_end_watering = ? 
            WHERE id_owner = ? AND id_bed = ?
            ''',
            (self._time_end_watering, self._id, self._id_bed, )
        )
        self._db.commit()

    def upgrade_disease_resistance(self, id, id_bed):
        self._id = id
        self._id_bed = id_bed

        self._cursor.execute('SELECT chance_resistance FROM bed WHERE id_owner = ? AND id_bed = ?', (self._id, self._id_bed, ))
        self._result = self._cursor.fetchone()

        self._cursor.execute(
            '''
            UPDATE bed
            SET chance_resistance = chance_resistance - 1
            WHERE id_owner = ? AND id_bed = ?
            ''',
            (self._id, self._id_bed, )
        )
        self._db.commit()


    def upgrade_reducing_soil(self, id, id_bed):
        self._id = id
        self._id_bed = id_bed

        self._cursor.execute('SELECT watering_hours FROM bed WHERE id_owner = ? AND id_bed = ?', (self._id, self._id_bed, ))
        self._result = self._cursor.fetchone()

        self._cursor.execute(
            '''
            UPDATE bed
            SET watering_hours = watering_hours + 1
            WHERE id_owner = ? AND id_bed = ?
            ''',
            (self._id, self._id_bed, )
        )
        self._db.commit()

    def added_holes(self, id, id_bed, price):
        self._id = id
        self._id_bed = id_bed
        self._price = price

        self._cursor.execute(
            '''
            UPDATE bed
            SET holes = holes + 1, last_price_added_holes = ?
            WHERE id_owner = ? AND id_bed = ?
            ''',
            (self._price, self._id, self._id_bed, )
        )
        self._db.commit()


    def get_items(self):
        self._cursor.execute(
            '''
            SELECT *
            FROM items
            '''
        )
        return self._cursor.fetchall()
    
    def get_items_name(self, name_item):
        self._name_item = name_item

        self._cursor.execute('SELECT * FROM items WHERE name = ?', (self._name_item, ))
        return self._cursor.fetchone()


    def get_items_id(self, id_item):
        self._id_item = id_item
        self._cursor.execute(
            '''
            SELECT *
            FROM items
            WHERE item_id = ?
            ''',
            (self._id_item, )
        )
        return self._cursor.fetchone()

    def get_tool_rake(self, id):
        self._id = id
        self._cursor.execute(
            '''
            SELECT tool_id
            FROM tool
            JOIN items ON tool.tool_id = items.item_id
            WHERE id = ? AND items.type = 'грабли'
            ''',
            (self._id, )
        )
        return self._cursor.fetchone()
    
    def get_rake(self, id):
        self._id = id
        self._cursor.execute(
            '''
            SELECT tool.tool_id, items.name, tool.strength
            FROM tool
            JOIN items ON tool.tool_id = items.item_id
            WHERE id = ? AND items.type = 'грабли'
            ''',
            (self._id, )
        )
        return self._cursor.fetchone()

    def set_tool(self, id, tool_id, strength):
        self._id = id
        self._tool_id = tool_id
        self._strength = strength
        
        self._cursor.execute(
            '''
            INSERT INTO tool (id, tool_id, strength)
            VALUES (?, ?, ?)
            ''',
            (self._id, self._tool_id, self._strength, )
        )
        self._db.commit()

    def remove_tool(self, id, tool_id):
        self._id = id
        self._tool_id = tool_id
        self._cursor.execute(
            '''
            DELETE FROM tool
            WHERE id = ? AND tool_id = ?
            ''',
            (self._id, self._tool_id, )
        )
        self._db.commit()

    def edit_tool(self, id, tool_id):
        self._id = id
        self._tool_id = tool_id

        self._cursor.execute(
            '''
            SELECT strength FROM tool WHERE id = ? AND tool_id = ?
            ''',
            (self._id, self._tool_id, )
        )
        if self._cursor.fetchone()['strength'] == 1:
            self._cursor.execute(
                '''
                DELETE FROM tool
                WHERE id = ? AND tool_id = ?
                ''',
                (self._id, self._tool_id, )
            )
        else:
            self._cursor.execute(
                '''
                UPDATE tool
                SET strength = strength - 1
                WHERE id = ? AND tool_id = ?
                ''',
                (self._id, self._tool_id, )
            )
        self._db.commit()
    
    
    def set_tasks(self, id, tasks):
        self._id = id
        self._tasks = tasks
        self._task1 = self._tasks[0]
        self._task2 = self._tasks[1]

        self._cursor.execute('SELECT id FROM tasks WHERE id = ?', (self._id, ))
        result = self._cursor.fetchone()

        if result != None:
            self._cursor.execute(
                '''
                UPDATE tasks
                SET text_task1 = ?,
                    task1 = ?,
                    plant1 = ?,
                    task1_completed = 0,
                    text_task2 = ?,
                    task2 = ?, 
                    plant2 = ?,
                    task2_completed = 0,
                    get_reward = 0
                WHERE id = ?
                ''',
                (
                    self._task1['text'], self._task1['required'], self._task1['plant'],
                    self._task2['text'], self._task2['required'], self._task2['plant'],
                    self._id, 
                )
            )
        else:
            self._cursor.execute(
                '''
                INSERT INTO tasks 
                (id, text_task1, task1, plant1, task1_completed, text_task2, task2, plant2, task2_completed, get_reward)
                VALUES
                (?, ?, ?, ?, 0, ?, ?, ?, 0, 0)
                ''',
                (
                    self._id, 
                    self._task1['text'], self._task1['required'], self._task1['plant'],
                    self._task2['text'], self._task2['required'], self._task2['plant'],
                )
            )
        self._db.commit()

    def get_tasks(self, id):
        self._id = id

        self._cursor.execute(
            '''
            SELECT * FROM tasks WHERE id = ?
            ''',
            (self._id, )
        )
        return self._cursor.fetchone()

    def get_info_for_tasks(self, id):
        self._id = id

        self._cursor.execute(
            '''
            SELECT farm.amount_beds, bed.holes
            FROM farm
            JOIN bed ON farm.id = bed.id_owner
            WHERE id = ?
            ''',
            (self._id, )
        )
        return self._cursor.fetchall()
    
    def update_completed_task(self, id, task_id, quantity):
        self._id = id
        self._task_id = task_id
        self._quantity = quantity

        if self._task_id == 1:
            self._cursor.execute(
                '''
                UPDATE tasks
                SET task1_completed = task1_completed + ?
                WHERE id = ?
                ''',
                (self._quantity, self._id, )
            )
        if self._task_id == 2:
            self._cursor.execute(
                '''
                UPDATE tasks
                SET task2_completed = task2_completed + ?
                WHERE id = ?
                ''',
                (self._quantity, self._id, )
            )

        self._cursor.execute(
            '''
            SELECT * FROM tasks WHERE id = ?
            ''',
            (self._id, )
        )
        self._result = self._cursor.fetchone()

        if self._result['task1'] <= self._result['task1_completed']:
            self._cursor.execute(
                '''
                UPDATE tasks
                SET task1_completed = -1
                WHERE id = ? 
                ''',
                (self._id,)
            )
        if self._result['task2'] <= self._result['task2_completed']:
            self._cursor.execute(
                '''
                UPDATE tasks
                SET task2_completed = -1
                WHERE id = ? 
                ''',
                (self._id,)
            )
        self._db.commit()

    def edit_get_reward(self, id):
        self._id = id

        self._cursor.execute(
            '''
            UPDATE tasks
            SET get_reward = 1
            WHERE id = ?
            ''',
            (self._id, )
        )
        self._db.commit()


    # Casino
    def set_casino(self, id):
        self._id = id 

        self._cursor.execute('SELECT id FROM casino WHERE id = ?', (self._id, ))
        self._result = self._cursor.fetchone()

        if self._result == None:
            self._cursor.execute(
                '''
                INSERT INTO casino (id, bid)
                VALUES (?, 10)
                ''',
                (self._id, )
            )
        else:
            self._cursor.execute(
                '''
                UPDATE casino
                SET bid = 10
                WHERE id = ?
                ''',
                (self._id, )
            )
        self._db.commit()
    
    def update_bid(self, id, bid, action):
        self._id = id
        self._bid = bid
        self._action = action

        self._cursor.execute(
            f'''
            UPDATE casino
            SET bid = ? {self._action}
            WHERE id = ?
            ''',
            (self._bid, self._id)
        )
        self._db.commit()

    def get_casino(self, id):
        self._id = id

        self._cursor.execute('SELECT * FROM casino WHERE id = ?', (self._id,))
        return self._cursor.fetchone()
    

    def set_product(self, id_owner, id_item, price, quantity):
        self._id_owner = id_owner
        self._id_item = id_item
        self._price = price
        self._quantity = quantity

        self._cursor.execute('''
            INSERT INTO market (id_owner, id_item, price, quantity, message_id)
            VALUES (?, ?, ?, ?, 0)
            ''', 
            (self._id_owner, self._id_item, self._price, self._quantity, )
        )
        listing_id = self._cursor.lastrowid
        self._db.commit()
        return listing_id
    
    def set_message_id_product(self, id_product, message_id):
        self._id_product = id_product
        self._message_id = message_id

        self._cursor.execute(
            '''
            UPDATE market
            SET message_id = ?
            WHERE id = ?
            ''',
            (self._message_id, self._id_product, )
        )
        self._db.commit()

    def get_product(self, id):
        self._id = id

        self._cursor.execute(
            '''
            SELECT *
            FROM market 
            WHERE id = ?
            ''', 
            (self._id,)
        )
        return self._cursor.fetchone()
    
    def get_products_user(self, id):
        self._id = id 

        self._cursor.execute(
            '''
            SELECT *
            FROM market
            WHERE id_owner = ?
            ''',
            (self._id, )
        )
        return self._cursor.fetchall()

    def delete_product(self, id):
        self._id = id

        self._cursor.execute(
            '''
            DELETE FROM market
            WHERE id = ?
            ''',
            (self._id, )
        )
        self._db.commit()

    
    def set_report(self, id_addressing, text, state = 0):
        self._id_addressing = id_addressing
        self._text = text
        self._state = state

        self._cursor.execute(
            '''
            INSERT INTO reports
            (id_addressing, text, state, id_supported)
            VALUES 
            (?, ?, ?, 0)
            ''',
            (self._id_addressing, self._text, self._state, )
        )
        id_report = self._cursor.lastrowid
        self._db.commit()
        return id_report

    def update_state_report(self, id, state, id_supported):
        '''
        state = 0 - Новое обращение\n
        state = 1 - Решается\n
        state = 2 - Отказано\n
        state = 3 - Решено
        '''
        self._id = id
        self._state = state
        self._id_supported = id_supported

        self._cursor.execute(
            '''
            UPDATE reports
            SET state = ?, id_supported = ?
            WHERE id = ?
            ''',
            (self._state, self._id_supported, self._id, )
        )
        self._db.commit()

    def get_report(self, id):
        self._id = id

        self._cursor.execute(
            '''
            SELECT * FROM reports WHERE id = ?
            ''',
            (self._id, )
        )
        return self._cursor.fetchone()
    
    def get_report_addressing(self, id_addressing):
        self._id_addressing = id_addressing

        self._cursor.execute(
            '''
            SELECT * FROM reports WHERE id_addressing = ? AND state IN (0, 1)
            ''',
            (self._id_addressing, )
        )
        return self._cursor.fetchall()
    
    
    def get_id_users_ready_harvest(self):
        self._cursor.execute(
            '''
            SELECT id_owner, id_bed, time_end
            FROM bed
            WHERE state = 1
            '''
        )
        return self._cursor.fetchall()
    
    def reset_daily_bonus(self):
        self._cursor.execute(
            '''
            UPDATE user
            SET daily_bonus = 0
            '''
        )
        self._db.commit()