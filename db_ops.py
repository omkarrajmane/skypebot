import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from database_setup import Base, Tasks, User, TaskMapping
import constants


class DatabaseOperations(object):
    """
     AAS the name suggests, here all the database operations take place
    """

    # TODO add exception handling
    def __init__(self):
        engine = create_engine(constants.DB_URL)
        Base.metadata.create_all(engine)

        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    @staticmethod
    def get_table_object(table_name):
        """
        This method returns the table Object for a given table name
        :param table_name: name of table (String)
        :return: Object of the table (Object)
        """
        table_object = None
        if table_name == constants.user_details_table:
            table_object = User
        elif table_name == constants.task_details_table:
            table_object = Tasks
        elif table_name == constants.task_mapping_table:
            table_object = TaskMapping
        return table_object

    def add_row(self, table_name, row_details):
        """
        Adds row in a given table
        :param table_name: name of table (String)
        :param row_details: dict containing key value pairs of attributes & corresponding values. (Dict)
        :return: Boolean
        """
        try:
            table_object = self.get_table_object(table_name)

            row_obj = table_object(**row_details)
            self.session.add(row_obj)
            self.session.commit()
            return row_obj
        except Exception as e:
            return "Error occured while adding row: {}. Error : {}".format(row_details, e)

    def read_table(self, table_name):
        """
        Read a given table
        :param table_name: name of table (String)
        :return: Table object (Object)
        """
        table_object = self.get_table_object(table_name)
        table = self.session.query(table_object)
        return table

    def get_row_with_query(self, table_name, query_dict):
        """
        Row with query
        :param table_name: name oof table
        :param query_dict: Dict of table attr as key and table value as value
        :return:
        """
        try:
            table_object = self.get_table_object(table_name=table_name)
            row = self.session.query(table_object).filter_by(**query_dict).one()
            return row
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    def delete_row_with_query(self, table_name, query_dict):
        """
        Deletes row from the given table
        :param table_name: table name from constants
        :param query: Dict of table attr as key and table value as value
        :return: True/ False
        """
        table_object = self.get_table_object(table_name=table_name)
        row_to_delete = self.session.query(table_object).filter_by(**query_dict).one()
        self.session.delete(row_to_delete)
        self.session.commit()
        return True

    def delete_row(self, row_obj):
        """
        Deletes row of the given row object
        :param row_obj: object of type Tasks or Users or TasksMapping (any table class) (Object)
        :return:
        """
        self.session.delete(row_obj)
        self.session.commit()
        return True

    def update_table(self, table_name, query_dict, update_dict):
        """

        :param table_name: name of table to update (String)
        :param query_dict: dict to query update. This dict should contain exact attribute names(Dict)
        :param update_dict: dict to update. This dict should contain exact attribute names(Dict)
        :return:
        """
        table_object = self.get_table_object(table_name=table_name)
        row_to_update = self.session.query(table_object).filter_by(**query_dict).one()
        for attribute, value in update_dict.items():
            # update non id fields and non None values
            if attribute not in constants.ID_FIELDS and value is not None:
                setattr(row_to_update, attribute, value)
        self.session.add(row_to_update)
        self.session.commit()
        return True

    def add_user_task_mapping(self, task_obj, user_obj):
        """
        This function adds mapping between tasks and users
        :param user_id: user id of user (String)
        :param task_id: task id of task (String)
        :return:
        """
        user_obj.tasks.append(task_obj)
        self.session.commit()
        return user_obj
