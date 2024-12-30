import json
from datetime import date

from config import HOST, USER, PASSWORD, DATABASE
import mysql.connector
import bcrypt


class DBConnectionMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MySQLConnection(metaclass=DBConnectionMeta):
    def __init__(self):
        config = {
            'host': HOST,
            'user': USER,
            'password': PASSWORD,
            'database': DATABASE,
            'raise_on_warnings': True
        }
        self._cnx = mysql.connector.connect(**config)

    def __del__(self):
        if self._cnx.is_connected():
            self._cnx.close()

    @property
    def cnx(self):
        return self._cnx


class AccountsDatabase:
    def __init__(self):
        self._db = MySQLConnection()
        self._cnx = self._db.cnx

    def register_user(self, data: dict) -> dict:
        login, password = data['login'], data['password']
        if not self._user_exists(login):
            with self._cnx.cursor() as cursor:
                query = "INSERT INTO accounts (login, password_hash) VALUES (%s, %s)"
                hashed_password = self._hash_password(password)
                cursor.execute(query, (login, hashed_password))
                self._cnx.commit()
            return {'status': 200, 'message': 'Успешная регистрация'}
        return {'status': 0, 'message': 'Такой пользователь уже существует'}

    def _user_exists(self, login: str) -> bool:
        """Проверить, существует ли пользователь в базе данных."""
        with self._cnx.cursor() as cursor:
            query = "SELECT COUNT(*) FROM accounts WHERE login = %s"
            cursor.execute(query, (login,))
            count = cursor.fetchone()[0]
        return count > 0

    def _get_user_password_hash(self, login: str) -> str:
        with self._cnx.cursor() as cursor:
            query = "SELECT password_hash FROM accounts WHERE login = %s"
            cursor.execute(query, (login,))
            result = cursor.fetchone()
        return result[0] if result else None

    def _get_user_avatar_name(self, login: str) -> str:
        with self._cnx.cursor() as cursor:
            query = "SELECT current_avatar_name FROM accounts WHERE login = %s"
            cursor.execute(query, (login,))
            result = cursor.fetchone()
            return result[0] if result else ''

    def upload_user_avatar(self, login: str, avatar_name: str) -> None:
        with self._cnx.cursor() as cursor:
            update_stmt = 'UPDATE accounts SET current_avatar_name = %s WHERE login = %s'
            cursor.execute(update_stmt, (avatar_name, login))
            self._cnx.commit()
            insert_stmt = 'INSERT INTO user_avatars (user_login, avatar_name) VALUES (%s, %s)'
            cursor.execute(insert_stmt, (login, avatar_name))
            self._cnx.commit()

    def edit_user_description_contacts(self, data):
        with self._cnx.cursor() as cursor:
            update_stmt = 'UPDATE accounts SET description = %s, contacts = %s WHERE login = %s'
            cursor.execute(update_stmt, (data['description_profile'], data['contacts'], data['login']))
            self._cnx.commit()
            return True

    def get_account_projects(self, data):
        with self._cnx.cursor() as cursor:
            query = "SELECT projects FROM accounts WHERE login = %s"
            cursor.execute(query, (data['login'],))
            result = cursor.fetchone()

            if result[0] is None:
                data['status'] = 404
                data['message'] = 'У данного пользователя нет проектов'
                return data

            project_names = list(map(str, result[0].split()))
            proj_db = ProjectsDatabase()
            account_projects = []

            for project in project_names:
                project_info = proj_db.get_project_by_name(project)
                account_projects.append(project_info)

            data['status'] = 200
            data['message'] = 'Всё гуд'

            for number, row in enumerate(account_projects):
                data['startups'][number + 1] = row

            return data

    def delete_project(self, project_id: int, login: str) -> bool:
        with self._cnx.cursor() as cursor:
            query = "SELECT project_name FROM projects WHERE id = %s"
            cursor.execute(query, (project_id,))
            result = cursor.fetchone()
            project_name = result[0]

            projects_query = "SELECT projects FROM accounts WHERE login = %s"
            cursor.execute(projects_query, (login,))
            projects_result = str(cursor.fetchone()[0])
            project_names = projects_result.split()

            for i in range(len(project_names)):
                if project_names[i] == project_name:
                    del project_names[i]
                    break

            refreshed_account_projects = ' '.join(project_names) if len(project_names) > 0 else None
            update_stmt = "UPDATE accounts SET projects = %s WHERE login = %s"
            cursor.execute(update_stmt, (refreshed_account_projects, login))
            self._cnx.commit()

            proj_db = ProjectsDatabase()
            proj_db.delete_project(project_id)

            return True

    def get_account_description_contacts(self, login: str) -> dict:
        with self._cnx.cursor() as cursor:
            query = 'SELECT description, contacts FROM accounts WHERE login = %s'
            cursor.execute(query, (login,))
            result = cursor.fetchone()
            account_info = {
                'description_profile': result[0],
                'contacts': result[1]
            }
            return account_info


    def authenticate_user(self, data: dict) -> dict:
        login, password = data['login'], data['password']
        if self._user_exists(login):
            stored_hash = self._get_user_password_hash(login)
            if stored_hash and self._check_password(stored_hash, password):
                account_info = self.get_account_description_contacts(login)                   

                if account_info['description_profile'] == None:
                    account_info['description_profile'] = ''
                
                if account_info['contacts'] == None:
                    account_info['contacts'] = ''

                return {
                    'status': 200, 
                    'icon': self._get_user_avatar_name(login), 
                    'description_profile': account_info['description_profile'],
                    'contacts': account_info['contacts']
                }
        return {'status': 403, 'icon': ''}

    @staticmethod
    def _hash_password(password: str) -> str:
        """Хэшировать пароль."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def _check_password(stored_hash: str, password: str) -> bool:
        """Проверить пароль."""
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))


class ProjectsDatabase:
    def __init__(self):
        self._db = MySQLConnection()
        self._cnx = self._db.cnx

    @staticmethod
    def _create_query_filter(data: dict, is_default: bool = True) -> str:
        projects = 5
        query_template = 'SELECT project_name, description, likes, id FROM projects'

        # index_action:
        # 0 - most likes
        # 1 - most recent
        # 2 - less recent
        # 3 - fewer likes
        query_filter = ''

        match data['index_action']:
            case 0:
                query_filter = "ORDER BY likes DESC"
            case 1:
                query_filter = "ORDER BY foundation_date DESC"
            case 2:
                query_filter = "ORDER BY foundation_date"
            case 3:
                query_filter = "ORDER BY likes"

        offset = len(data['project_ids'])

        if is_default:
            return f"{query_template} {query_filter} LIMIT {projects} OFFSET {offset}"

        query = f"{query_template} WHERE project_name REGEXP %s {query_filter} LIMIT {projects} OFFSET {offset}"

        return query

    def get_project_by_name(self, project_name: str) -> dict:
        with self._cnx.cursor() as cursor:
            query = 'SELECT description, likes, id FROM projects WHERE project_name = %s'
            cursor.execute(query, (project_name,))
            result = cursor.fetchone()
            if result:
                project = {
                    'project_name': project_name,
                    'description': result[0],
                    'likes': result[1],
                    'id': result[2]
                }
                return project

    def _execute_query_filter(self, data: dict, query: str):
        with self._cnx.cursor() as cursor:
            if 'name_project' in data and data['name_project']:
                cursor.execute(query, (data['name_project'],))
            else:
                cursor.execute(query)
            result = cursor.fetchall()

            if result:
                data['status'] = 200
                data['message'] = 'Всё гуд'

                for number, row in enumerate(result):
                    number += 1
                    project_info = {
                        'name': row[0],
                        'description': row[1],
                        'likes': row[2],
                        'id': row[3]
                    }
                    data['startups'][number] = project_info
            else:
                data['status'] = 0
                data['message'] = 'Не удалось загрузить данные о проектах'

            return data

    def getprojectdata(self, data: dict, project_id: int) -> dict:
        with self._cnx.cursor() as cursor:
            query = "SELECT project_name, description, contacts FROM projects WHERE id = %s"
            cursor.execute(query, (project_id,))
            result = cursor.fetchone()

            result_data = data.copy()
            result_data['status'] = 200
            result_data['message'] = 'Всё гуд'
            result_data['name_project'] = result[0]
            result_data['description'] = result[1]
            result_data['contacts'] = result[2]

            return result_data

    def get_next_five_projects(self, data: dict) -> dict:
        if 'name_project' in data and data['name_project']:
            query = self._create_query_filter(data, is_default=False)
        else:
            query = self._create_query_filter(data)
        processed_projects_data = self._execute_query_filter(data, query)
        return processed_projects_data

    def like_project(self, data: dict) -> dict:
        login, project_name = data['login'], data['project_name']
        with self._cnx.cursor() as cursor:
            if self.check_if_liked(data):
                self.unlike_project(data)
            else:
                like_statement = "INSERT INTO likes (user, project_name) VALUES (%s, %s)"
                cursor.execute(like_statement, (login, project_name))

                project_statement = "UPDATE projects SET likes = likes + 1 WHERE project_name = %s"
                cursor.execute(project_statement, (project_name,))

                self._cnx.commit()

        return {'status': 200, 'message': 'Успешная операция', 'likes': self.get_project_likes(project_name)}

    def delete_project(self, project_id: int) -> bool:
        with self._cnx.cursor() as cursor:
            delete_stmt = 'DELETE FROM projects WHERE id = %s'
            cursor.execute(delete_stmt, (project_id,))
            self._cnx.commit()
            return True

    def _project_exists(self, project_name: str) -> bool:
        """Проверить, существует ли пользователь в базе данных."""
        with self._cnx.cursor() as cursor:
            query = "SELECT COUNT(*) FROM projects WHERE project_name = %s"
            cursor.execute(query, (project_name,))
            count = cursor.fetchone()[0]
        return count > 0

    def upload_project(self, data: dict) -> dict:
        with self._cnx.cursor() as cursor:
            if not self._project_exists(data['name_project']):
                upload_stmt = "INSERT INTO projects (project_name, description, foundation_date) VALUES (%s, %s, %s)"
                cursor.execute(upload_stmt, (data['name_project'], data['description'], date.today()))
                self._cnx.commit()
                update_stmt = "UPDATE accounts SET projects = IF(projects IS NULL, %s, CONCAT(projects, ' ', %s)) WHERE login = %s"
                cursor.execute(update_stmt, (data['name_project'], data['name_project'], data['login']))
                self._cnx.commit()
                return {'status': 200, 'message': 'Успешно добавлен проект'}
            return {'status': 403, 'message': 'Проект с таким именем уже существует'}

    def _find_project(self, project_name: str) -> bool:
        with self._cnx.cursor() as cursor:
            query = "SELECT COUNT(*) FROM projects WHERE project_name = %s"
            cursor.execute(query, (project_name,))
            count = cursor.fetchone()[0]
        return count > 0

    def get_project_likes(self, project):
        with self._cnx.cursor() as cursor:
            query = "SELECT likes FROM projects WHERE project_name = %s"
            cursor.execute(query, (project,))
            return cursor.fetchone()[0]

    def unlike_project(self, data: dict):
        login, project_name = data['login'], data['project_name']
        with self._cnx.cursor() as cursor:
            like_statement = "DELETE FROM likes WHERE user = %s AND project_name = %s"
            cursor.execute(like_statement, (login, project_name))

            project_statement = "UPDATE projects SET likes = likes - 1 WHERE project_name = %s"
            cursor.execute(project_statement, (project_name,))

            self._cnx.commit()

    def check_if_liked(self, data: dict) -> bool:
        login, project_name = data['login'], data['project_name']
        with self._cnx.cursor() as cursor:
            if self._find_project(project_name):
                query = "SELECT COUNT(*) FROM likes WHERE project_name = %s AND user = %s"
                cursor.execute(query, (project_name, login))
                count = cursor.fetchone()[0]
                return count > 0


if __name__ == '__main__':
    adb = AccountsDatabase()
    pdb = ProjectsDatabase()

    print(json.dumps(adb.get_account_projects({'login': 'ivan', 'startups': {}}), indent=4))
