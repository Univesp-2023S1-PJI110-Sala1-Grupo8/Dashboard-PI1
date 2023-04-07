import mysql.connector
from base_repository import BaseRepository
from model.user_model import User
from model.profile_model import Profile

class UserRepository(BaseRepository):
    """User repository class responsible for maintain persisted user entities."""

    USER_REPO_SQL_DQL_GET_ALL_USERS     = "SELECT u.id, u.nome, u.sobrenome, u.email, u.senha, u.perfil_id, p.descricao FROM usuario u INNER JOIN perfil p ON p.id = u.perfil_id"
    USER_REPO_SQL_DQL_GET_USER_BY_ID    = "SELECT u.id, u.nome, u.sobrenome, u.email, u.senha, u.perfil_id, p.descricao FROM usuario u INNER JOIN perfil p ON p.id = u.perfil_id WHERE u.id = %s"
    USER_REPO_SQL_DQL_GET_USER_BY_EMAIL = "SELECT u.id, u.nome, u.sobrenome, u.email, u.senha, u.perfil_id, p.descricao FROM usuario u INNER JOIN perfil p ON p.id = u.perfil_id WHERE u.email = %s"
    USER_REPO_SQL_DML_INSERT_USER       = "INSERT INTO usuario (nome, sobrenome, email, senha, perfil_id) VALUES (%s, %s, %s, %s, %s)"
    USER_REPO_SQL_DML_UPDATE_USER       = "UPDATE usuario SET nome = %s, sobrenome = %s, email = %s, senha = %s, perfil_id = %s WHERE id = %s"
    USER_REPO_SQL_DML_DELETE_USER       = "DELETE FROM usuario WHERE email = %s"

    def __init__(self, database):
        super().__init__(database)

    def insert_user(self, user):
        try:
            existing_user = self.find_user_by_email(user.email)
            if existing_user is not None:
                raise Exception("User with this email already exists (id = {})".format(existing_user.id))
            cursor = self.db.conn.cursor()
            cursor.execute(self.USER_REPO_SQL_DML_INSERT_USER, (
                user.first_name, user.last_name, user.email, user.password, user.profile.id))
            cursor.close()
            inserted_user = self.find_user_by_email(user.email)
            if inserted_user is None:
                raise Exception("User has not been inserted.")
            self.db.conn.commit()
            return inserted_user
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def update_user(self, user):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.USER_REPO_SQL_DML_UPDATE_USER, (
                user.first_name, user.last_name, user.email, user.password, user.profile.id, user.id))
            cursor.close()
            self.db.conn.commit()
            return self.find_user_by_id(user.id)
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def delete_user(self, user_email):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.USER_REPO_SQL_DML_DELETE_USER, (user_email,))
            cursor.close()
            self.db.conn.commit()
            return True
        except mysql.connector.Error as err:
            self.report_error(err)
        return False

    def find_user_by_id(self, id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.USER_REPO_SQL_DQL_GET_USER_BY_ID, (id,))
            row = cursor.fetchone()
            if row is None:
                return None
            profile = Profile(id=row[5], name=row[6])
            user = User(id=row[0], first_name=row[1], last_name=row[2],
                        email=row[3], password=row[4], profile=profile)
            cursor.close()
            return user
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def find_user_by_email(self, email):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.USER_REPO_SQL_DQL_GET_USER_BY_EMAIL, (email,))
            row = cursor.fetchone()
            if row is None:
                return None
            profile = Profile(id=row[5], name=row[6])
            user = User(id=row[0], first_name=row[1], last_name=row[2],
                        email=row[3], password=row[4], profile=profile)
            cursor.close()
            return user
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def get_all_users(self):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.USER_REPO_SQL_DQL_GET_ALL_USERS)
            result_list = []
            for (user_id, user_firstname, user_lastname, user_email, user_pass, profile_id, profile_desc) in cursor:
                profile = Profile(id=profile_id, name=profile_desc)
                user = User(id=user_id, first_name=user_firstname, last_name=user_lastname,
                            email=user_email, password=user_pass, profile=profile)
                result_list.append(user)
            cursor.close()
            return result_list
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

