import sqlite3
from abc import ABC, abstractmethod


class DatabaseError(Exception):
    pass


class BaseSqlite(ABC):
    def __init__(self, db_addr):
        self.db_addr = db_addr
        self.con = sqlite3.connect(self.db_addr)
        self.cur = self.con.cursor()

    @property
    @abstractmethod
    def insert_query(self):
        pass

    @property
    @abstractmethod
    def update_query(self):
        pass

    @property
    @abstractmethod
    def read_db_query(self):
        pass

    @property
    @abstractmethod
    def read_query(self):
        pass

    def insert_to_db(self, query, params=()):
        try:
            self.cur.execute(query, params)
            if self.cur.rowcount:
                print(f'кол-во строк - {self.cur.rowcount}')
                last_id = self.cur.lastrowid
                print(f'last - {last_id}')
                self.con.commit()
                if not last_id:
                    return True
                return last_id
        except Exception as error:
            raise DatabaseError(
                'Что-то с базой, наверное занята...'
            ) from error

    def read_db(self, query, params=()):
        res = self.cur.execute(query, params)
        return res.fetchall()

    def close_db(self):
        self.con.close()


class OutQueryDb(BaseSqlite):
    def __init__(self, db_addr):
        super().__init__(db_addr)

        create_querys_table = '''
        CREATE TABLE IF NOT EXISTS queries(
            id INTEGER PRIMARY KEY,
            date_reg TEXT DEFAULT (DATE('now')),
            num_query TEXT,
            date_query TEXT,
            to_sfr TEXT,
            snils TEXT,
            fio TEXT,
            name_org TEXT,
            work_period TEXT,
            due_date TEXT,
            type_query TEXT,
            date_answer TEXT,
            spec TEXT
        );
        '''
        create_users_table = '''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            name TEXT
        );
        '''
        self.cur.execute(create_querys_table)
        self.cur.execute(create_users_table)
        self.con.commit()

    @property
    def insert_query(self):
        return '''
        INSERT INTO queries (
            date_reg,
            num_query,
            date_query,
            to_sfr,
            snils,
            fio,
            name_org,
            work_period,
            due_date,
            type_query,
            date_answer,
            spec
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

    @property
    def update_query(self):
        return '''
        UPDATE queries SET
            date_reg = ?,
            num_query = ?,
            date_query = ?,
            to_sfr = ?,
            snils = ?,
            fio = ?,
            name_org = ?,
            work_period = ?,
            due_date = ?,
            type_query = ?,
            date_answer = ?,
            spec = ?
        WHERE id = ?
        '''

    @property
    def read_db_query(self):
        return 'SELECT * FROM queries'

    @property
    def read_query(self):
        return 'SELECT * FROM queries WHERE snils = ?'

    @property
    def read_query_fo_id(self):
        return 'SELECT * FROM queries WHERE id = ?'

    @property
    def create_user(self):
        return 'INSERT INTO users (name) VALUES (?)'

    @property
    def delete_user(self):
        return 'DELETE FROM users WHERE name = ?'

    def last_record_id(self):  # этот метод вроде как не нужен
        res = self.cur.execute(
            '''
            SELECT id
            FROM queries
            ORDER BY id
            DESC LIMIT 1
            '''
        )
        return res.fetchone()[0]

    def users_list(self):
        res = self.cur.execute('SELECT * FROM users')
        return res.fetchall()


if __name__ == '__main__':
    gur_zapr = OutQueryDb('db.sqlite')
