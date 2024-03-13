import sqlite3
from config import DATABASE

skills = [ (_,) for _ in (['Python', 'SQL', 'API'])]
statuses = [ (_,) for _ in (['На этапе проектирования', 'В процессе разработки', 'Разработан. Готов к использованию.', 'Обновлен', 'Завершен. Не поддерживается'])]

class DB_Manager:
    def __init__(self, database):
        self.database = database

    def create_tables(self):
        # Устанавливаем соединение с базой данных
        conn = sqlite3.connect(self.database)

        with conn:
            # Создаем таблицу projects
            conn.execute('''CREATE TABLE projects (
                            project_id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            project_name TEXT NOT NULL,
                            description TEXT,
                            url TEXT,
                            status_id INTEGER,
                            FOREIGN KEY(status_id) REFERENCES status(status_id)
                        )''') 

            # Создаем таблицу skills
            conn.execute('''CREATE TABLE skills (
                            skill_id INTEGER PRIMARY KEY,
                            skill_name TEXT
                        )''')

            # Создаем связующую таблицу project_skills
            conn.execute('''CREATE TABLE project_skills (
                            project_id INTEGER,
                            skill_id INTEGER,
                            FOREIGN KEY(project_id) REFERENCES projects(project_id),
                            FOREIGN KEY(skill_id) REFERENCES skills(skill_id)
                        )''')
            
            conn.execute('''CREATE TABLE status (
                            status_id INTEGER PRIMARY KEY,
                            status_name TEXT
                        )''')

            # Сохраняем изменения и закрываем соединение
            conn.commit()

        print("База данных успешно создана.")

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)

    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()



    def default_insert(self):
        sql = 'INSERT INTO skills (skill_name) values(?)'
        data = skills
        self.__executemany(sql, data)
        sql = 'INSERT INTO status (status_name) values(?)'
        data = statuses
        self.__executemany(sql, data)



    def insert_project(self, data):
        sql = 'INSERT INTO projects (user_id, project_name, url, status_id) values(?, ?, ?, ?)'
        self.__executemany(sql, [data])

    def insert_skill(self, user_id, project_id, skill_id):
        sql = 'INSERT INTO project_skills VALUES(?, ?)'
        self.__executemany(sql, [(user_id, project_id, skill_id)])


  
    def get_statuses(self):
        sql='SELECT status_name from status'
        return self.__select_data(sql)

    def get_project_id(self, project_name, user_id):
        sql = 'SELECT project_id FROM projects WHERE project_name = ? AND user_id = ?'
        res = self.__select_data(sql, (project_name, user_id))[0][0]
        return res
        
    def get_status_id(self, status_name):
        sql = 'SELECT status_id FROM status WHERE status_name = ?'
        res = self.__select_data(sql, (status_name,))
        if res: return res[0][0]
        else: return None

    def get_projects(self, user_id):
        return self.__select_data(sql='SELECT * FROM projects WHERE user_id = ?', data = (user_id,))

    def get_skills(self):
        return self.__select_data(sql='SELECT * FROM skills')
    
    def get_project_info(self, user_id, project_name):
        sql = """
SELECT project_name, description, url, status_name FROM  (
SELECT * FROM projects 
JOIN status ON
status.status_id = projects.status_id)
WHERE project_name=? AND user_id=?
"""
        return self.__select_data(sql=sql, data = (project_name, user_id))[0]
    


    def update_projects(self, param, data):
        self.__executemany(f"UPDATE projects SET {param} = ? WHERE project_name = ? AND user_id = ?", [data]) # data ('atr', 'mew', 'name', 'user_id')


    def delete_project(self, user_id, project_id):
        sql = "DELETE FROM projects WHERE user_id = ? AND project_id = ? "
        self.__executemany(sql, [(user_id, project_id)])

    def delete_skill(self, project_id, skill_id):
        sql = "DELETE FROM skills WHERE skill_id = ? AND project_id = ? "
        self.__executemany(sql, [(skill_id, project_id)])


if __name__ == '__main__':
    manager = DB_Manager(DATABASE)

