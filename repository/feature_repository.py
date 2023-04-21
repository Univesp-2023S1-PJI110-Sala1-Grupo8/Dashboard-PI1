import mysql.connector
from model.feature_model import Feature
from model.feature_model import Feature
from repository.base_repository import BaseRepository


class FeatureRepository(BaseRepository):
    """
    Feature repository class responsible for maintain persisted features entities
    """

    FEATURE_REPO_SQL_DQL_GET_ALL_FEATURES    = "SELECT id, nome, nome_curto, descricao, estimativa_conclusao, percentual_conclusao, status, categoria_id, projeto_id FROM funcionalidade WHERE categoria_id = %s"
    FEATURE_REPO_SQL_DQL_GET_FEATURE_BY_ID   = "SELECT id, nome, nome_curto, descricao, estimativa_conclusao, percentual_conclusao, status, categoria_id, projeto_id FROM funcionalidade WHERE id = %s"
    FEATURE_REPO_SQL_DQL_GET_FEATURE_BY_NAME = "SELECT id, nome, nome_curto, descricao, estimativa_conclusao, percentual_conclusao, status, categoria_id, projeto_id FROM funcionalidade WHERE nome = %s and projeto_id = %s"
    FEATURE_REPO_SQL_DML_INSERT_FEATURE      = "INSERT INTO funcionalidade (nome, nome_curto, descricao, estimativa_conclusao, percentual_conclusao, status, categoria_id, projeto_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    FEATURE_REPO_SQL_DML_UPDATE_FEATURE      = "UPDATE funcionalidade SET nome = %s, nome_curto = %s, descricao = %s, estimativa_conclusao = %s, percentual_conclusao = %s, status = %s WHERE id = %s"
    FEATURE_REPO_SQL_DML_DELETE_FEATURE      = "DELETE FROM funcionalidade WHERE id = %s"

    def __init__(self, database):
        super().__init__(database)

    def insert_feature(self, feature, category_id, project_id):
        try:
            existing_feature = self.find_feature_in_project_by_name(feature.name, project_id)
            if existing_feature is not None:
                raise Exception("Feature with this name already exists in project (id = {})".format(existing_feature.id))
            if feature.estimated_end_date == '':
                feature.estimated_end_date = None;
            cursor = self.db.conn.cursor()
            cursor.execute(self.FEATURE_REPO_SQL_DML_INSERT_FEATURE,
                           (feature.name, feature.short_name, feature.description, feature.estimated_end_date,
                            feature.percent_done, feature.status, category_id, project_id))
            cursor.close()
            inserted_feature = self.find_feature_in_project_by_name(feature.name, project_id)
            if inserted_feature is None:
                raise Exception("Feature has not been inserted.")
            self.db.conn.commit()
            return inserted_feature
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def update_feature(self, feature):
        try:
            if feature.estimated_end_date == '':
                feature.estimated_end_date = None;
            cursor = self.db.conn.cursor()
            cursor.execute(self.FEATURE_REPO_SQL_DML_UPDATE_FEATURE,
                           (feature.name, feature.short_name, feature.description, feature.estimated_end_date,
                            feature.percent_done, feature.status, feature.id))
            cursor.close()
            self.db.conn.commit()
            return self.find_feature_by_id(feature.id)
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def delete_feature(self, feature_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.FEATURE_REPO_SQL_DML_DELETE_FEATURE, (feature_id,))
            cursor.close()
            self.db.conn.commit()
            return True
        except mysql.connector.Error as err:
            self.report_error(err)
        return False

    def find_feature_by_id(self, feature_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.FEATURE_REPO_SQL_DQL_GET_FEATURE_BY_ID, (feature_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            feature = Feature(id=row[0], name=row[1], short_name=row[2], description=row[3],
                              estimated_end_date=row[4], percent_done=row[5], status=row[6])
            if feature.estimated_end_date is None:
                feature.estimated_end_date = ''
            cursor.close()
            return feature
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def find_feature_in_project_by_name(self, feature_name, project_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.FEATURE_REPO_SQL_DQL_GET_FEATURE_BY_NAME, (feature_name, project_id))
            row = cursor.fetchone()
            if row is None:
                return None
            feature = Feature(id=row[0], name=row[1], short_name=row[2], description=row[3],
                              estimated_end_date=row[4], percent_done=row[5], status=row[6])
            if feature.estimated_end_date is None:
                feature.estimated_end_date = ''
            cursor.close()
            return feature
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

    def get_all_features_in_category(self, category_id):
        try:
            cursor = self.db.conn.cursor()
            cursor.execute(self.FEATURE_REPO_SQL_DQL_GET_ALL_FEATURES, (category_id,))
            resultList = []
            for (feature_id, feature_name, feature_shortname, feature_descr, feature_enddate,
                 feature_percentdone, feature_status, category_id, project_id) in cursor:
                feature = Feature(id=feature_id, name=feature_name, short_name=feature_shortname,
                                  description=feature_descr, percent_done=feature_percentdone,
                                  estimated_end_date=feature_enddate, status=feature_status)
                if feature.estimated_end_date is None:
                    feature.estimated_end_date = ''
                resultList.append(feature)
            cursor.close()
            return resultList
        except mysql.connector.Error as err:
            self.report_error(err)
        return None

