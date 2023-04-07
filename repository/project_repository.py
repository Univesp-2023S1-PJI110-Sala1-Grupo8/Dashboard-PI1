import mysql.connector
from model.project_model import Project
from model.feature_model import Feature
from model.category_model import Category
from repository.base_repository import BaseRepository
from repository.user_repository import UserRepository


class ProjectRepository(BaseRepository):
    """
    Project repository class responsible for maintain persisted project entities
    along with features and categories.
    """
    PROJECT_REPO_SQL_DQL_GET_ALL_PROJECTS        = "SELECT id, nome, nome_curto, descricao, percentual, status, usuario_id FROM projeto WHERE usuario_id = %s"
    PROJECT_REPO_SQL_DQL_GET_PROJECT_BY_ID       = "SELECT id, nome, nome_curto, descricao, percentual, status, usuario_id FROM projeto WHERE id = %s"
    PROJECT_REPO_SQL_DQL_GET_PROJECT_BY_SNAME    = "SELECT id, nome, nome_curto, descricao, percentual, status, usuario_id FROM projeto WHERE nome_curto = %s"
    PROJECT_REPO_SQL_DML_INSERT_PROJECT          = "INSERT INTO projeto (nome, nome_curto, descricao, percentual, status, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)"
    PROJECT_REPO_SQL_DML_UPDATE_PROJECT          = "UPDATE projeto SET nome = %s, nome_curto = %s, descricao = %s, percentual = %s, status = %s WHERE id = %s"
    PROJECT_REPO_SQL_DML_DELETE_PROJECT          = "DELETE FROM projeto WHERE id = %s"
    PROJECT_REPO_SQL_DML_DELETE_BY_SNAME_PROJECT = "DELETE FROM projeto WHERE nome_curto = %s"

    def __init__(self, database):
        super().__init__(database)
        self.user_repository = UserRepository(database)

    def insert_project(self, project):
        try:
            existing_project = self.find_project_by_shortname(project.short_name)
            if existing_project is not None:
                raise Exception("Project with this short name already exists (id = {})".format(existing_project.id))
            cursor = self.db.conn.cursor()
            cursor.execute(self.PROJECT_REPO_SQL_DML_INSERT_PROJECT, (
                project.name, project.short_name, project.description,
                project.percent_done, project.status, project.owner.id))
            cursor.close()
            inserted_project = self.find_project_by_shortname(project.short_name)
            if inserted_project is None:
                raise Exception("Project has not been inserted.")
            self.db.conn.commit()
            return inserted_project
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def update_project(self, project):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.PROJECT_REPO_SQL_DML_UPDATE_PROJECT, (
                project.name, project.short_name, project.description,
                project.percent_done, project.status, project.id))
            cursor.close()
            self.db.conn.commit()
            return self.find_project_by_id(project.id)
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def delete_project(self, project_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.PROJECT_REPO_SQL_DML_DELETE_PROJECT, (project_id,))
            cursor.close()
            self.db.conn.commit()
            return True
        except mysql.connector.Error as err:
            self.report_error(err)
        return False

    def delete_project_by_shortname(self, project_shortname):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.PROJECT_REPO_SQL_DML_DELETE_PROJECT_BY_SNAME, (project_shortname,))
            cursor.close()
            self.db.conn.commit()
            return True
        except mysql.connector.Error as err:
            self.report_error(err)
        return False

    def find_project_by_id(self, project_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.PROJECT_REPO_SQL_DQL_GET_PROJECT_BY_ID, (project_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            owner = self.user_repository.find_user_by_id(row[6])
            if owner is None:
                raise Exception("Project Owner does not exist.")
            project = Project(id=row[0], name=row[1], short_name=row[2], description=row[3],
                              percent_done=row[4], status=row[5], owner=owner)
            cursor.close()
            return project
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def find_project_by_shortname(self, project_short_name):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.PROJECT_REPO_SQL_DQL_GET_PROJECT_BY_SNAME, (project_short_name,))
            row = cursor.fetchone()
            if row is None:
                return None
            owner = self.user_repository.find_user_by_id(row[6])
            if owner is None:
                raise Exception("Project Owner does not exist.")
            project = Project(id=row[0], name=row[1], short_name=row[2], description=row[3],
                              percent_done=row[4], status=row[5], owner=owner)
            cursor.close()
            return project
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def get_all_projects_of_user(self, user_id):
        try:
            user = self.user_repository.find_user_by_id(user_id)
            if user is None:
                raise Exception("User not found by id {}.".format(user_id))
            cursor = self.db.conn.cursor()
            cursor.execute(self.PROJECT_REPO_SQL_DQL_GET_ALL_PROJECTS)
            resultList = []
            for (project_id, project_name, project_shortname, project_descr, project_percent, project_status, user_id) in cursor:
                project = Project(id=project_id, name=project_name, short_name=project_shortname,
                                  description=project_descr, percent_done=project_percent,
                                  status=project_status, owner=user)
                resultList.append(project)
            cursor.close()
            return resultList
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

