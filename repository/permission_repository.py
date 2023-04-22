import mysql.connector
from repository.base_repository import BaseRepository
from repository.user_repository import UserRepository
from repository.project_repository import ProjectRepository

class PermissionRepository(BaseRepository):
    """
    Permission repository class responsible for maintain persisted user permission for project access
    """
    PERMISSION_REPO_SQL_DQL_GET_ALLOWED_USERS_FOR_PROJECT  = "SELECT up.usuario_id, up.projeto_id FROM usuario_permissao up INNER JOIN usuario u ON u.id = up.usuario_id WHERE up.projeto_id = %s ORDER BY u.nome, u.sobrenome ASC"
    PERMISSION_REPO_SQL_DQL_GET_PERMISSION_BY_USER_PROJECT = "SELECT usuario_id, projeto_id FROM usuario_permissao WHERE usuario_id = %s AND projeto_id = %s"
    PERMISSION_REPO_SQL_DQL_GET_PERMISSION_BY_USER         = "SELECT usuario_id, projeto_id FROM usuario_permissao WHERE usuario_id = %s"
    PERMISSION_REPO_SQL_DML_INSERT_USER_PERMISSION         = "INSERT INTO usuario_permissao (usuario_id, projeto_id, permissao) VALUES (%s, %s, 1)"
    PERMISSION_REPO_SQL_DML_DELETE_USER_PERMISSION         = "DELETE FROM usuario_permissao WHERE usuario_id =%s AND projeto_id = %s"

    def __init__(self, database):
        super().__init__(database)

    def insert_permission(self, user_id, project_id):
        try:
            existing_permission = self.find_permission(user_id, project_id)
            if existing_permission is not None:
                raise Exception("User {} has already permission to access the Project {}".format(
                    existing_permission[0], existing_permission[1]))
            cursor = self.db.conn.cursor()
            cursor.execute(self.PERMISSION_REPO_SQL_DML_INSERT_USER_PERMISSION, (user_id, project_id))
            cursor.close()
            inserted_permission = self.find_permission(user_id, project_id)
            if inserted_permission is None:
                raise Exception("Permission has not been inserted.")
            self.db.conn.commit()
            return inserted_permission
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def delete_permission(self, user_id, project_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.PERMISSION_REPO_SQL_DML_DELETE_USER_PERMISSION, (user_id, project_id))
            cursor.close()
            self.db.conn.commit()
            return True
        except mysql.connector.Error as err:
            self.report_error(err)
        return False

    def find_permission(self, user_id, project_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.PERMISSION_REPO_SQL_DQL_GET_PERMISSION_BY_USER_PROJECT, (user_id, project_id))
            row = cursor.fetchone()
            if row is None:
                return None
            permission = (row[0], row[1])
            cursor.close()
            return permission
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def get_allowed_users_in_project(self, project_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.PERMISSION_REPO_SQL_DQL_GET_ALLOWED_USERS_FOR_PROJECT, (project_id,))
            permission_list = []
            for (permission) in cursor:
                permission_list.append(permission)
            cursor.close()
            resultList = []
            user_repository = UserRepository(self.db)
            for (user_id, project_id) in permission_list:
                allowed_user = user_repository.find_user_by_id(user_id)
                if allowed_user is not None:
                    resultList.append(allowed_user)
            return resultList
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def get_allowed_projects_for_user(self, user_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.PERMISSION_REPO_SQL_DQL_GET_PERMISSION_BY_USER, (user_id,))
            permission_list = []
            for (permission) in cursor:
                permission_list.append(permission)
            cursor.close()
            resultList = []
            project_repository = ProjectRepository(self.db)
            for (user_id, project_id) in permission_list:
                granted_project = project_repository.find_project_by_id(project_id)
                if granted_project is not None:
                    resultList.append(granted_project)
            return resultList
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

