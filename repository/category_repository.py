import mysql.connector
from model.category_model import Category
from repository.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    """
    Category repository class responsible for maintain persisted categories entities
    """
    CATEGORY_REPO_SQL_DQL_GET_ALL_CATEGORIES   = "SELECT id, nome, projeto_id FROM categoria WHERE projeto_id = %s"
    CATEGORY_REPO_SQL_DQL_GET_CATEGORY_BY_ID   = "SELECT id, nome, projeto_id FROM categoria WHERE id = %s"
    CATEGORY_REPO_SQL_DQL_GET_CATEGORY_BY_NAME = "SELECT id, nome, projeto_id FROM categoria WHERE nome = %s and projeto_id = %s"
    CATEGORY_REPO_SQL_DML_INSERT_CATEGORY      = "INSERT INTO categoria (nome, projeto_id) VALUES (%s, %s)"
    CATEGORY_REPO_SQL_DML_UPDATE_CATEGORY      = "UPDATE categoria SET nome = %s WHERE id = %s"
    CATEGORY_REPO_SQL_DML_DELETE_CATEGORY      = "DELETE FROM categoria WHERE id = %s"

    def __init__(self, database):
        super().__init__(database)

    def insert_category(self, category, project_id):
        try:
            existing_category = self.find_category_in_project_by_name(category.name, project_id)
            if existing_category is not None:
                raise Exception("Category with this name already exists in project (id = {})".format(existing_category.id))
            cursor = self.db.conn.cursor()
            cursor.execute(self.CATEGORY_REPO_SQL_DML_INSERT_CATEGORY, (category.name, project_id))
            cursor.close()
            inserted_category = self.find_category_in_project_by_name(category.name, project_id)
            if inserted_category is None:
                raise Exception("Category has not been inserted.")
            self.db.conn.commit()
            return inserted_category
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def update_category(self, category):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.CATEGORY_REPO_SQL_DML_UPDATE_CATEGORY, (category.name,))
            cursor.close()
            self.db.conn.commit()
            return self.find_category_by_id(category.id)
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def delete_category(self, category_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.CATEGORY_REPO_SQL_DML_DELETE_CATEGORY, (category_id,))
            cursor.close()
            self.db.conn.commit()
            return True
        except mysql.connector.Error as err:
            self.report_error(err)
        return False

    def find_category_by_id(self, category_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.CATEGORY_REPO_SQL_DQL_GET_CATEGORY_BY_ID, (category_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            category = Category(id=row[0], name=row[1])
            cursor.close()
            return category
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def find_category_in_project_by_name(self, category_name, project_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.CATEGORY_REPO_SQL_DQL_GET_CATEGORY_BY_NAME, (category_name, project_id))
            row = cursor.fetchone()
            if row is None:
                return None
            category = Category(id=row[0], name=row[1])
            cursor.close()
            return category
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def get_all_categories_in_project(self, project_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.CATEGORY_REPO_SQL_DQL_GET_ALL_CATEGORIES, (project_id,))
            resultList = []
            for (category_id, category_name, project_id) in cursor:
                category = Category(id=category_id, name=category_name)
                resultList.append(category)
            cursor.close()
            return resultList
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

