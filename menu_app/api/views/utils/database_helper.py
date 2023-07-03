"""
Database Utility class and methods
"""

import re
from datetime import datetime
import getpass

from django.db import connection, DatabaseError


class DBUtils:
    """
    Database utility methods
    """
    @staticmethod
    def dict_fetchall(cursor):
        """
        Return all rows from a cursor as a dict
        :param cursor:
        :return dict of sql query results:
        """
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def execute_sql(self, sql):
        """
        Executes an arbitrary sql statement and returns a list of dict with the execution results
        :param sql string - can be a query or DML
        :return result list of dict
        """
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            # If a query is executed, then fetch result
            if re.search('SELECT', sql, re.IGNORECASE):
                result = self.dict_fetchall(cursor)
            else:
                result = None
        except ConnectionError as conn_err:
            raise ConnectionError("DB connection lost: " + str(conn_err)) from conn_err
        except DatabaseError as db_err:
            raise DatabaseError("DatabaseError : " + str(db_err)) from db_err
        finally:
            cursor.close()

        return result

    @staticmethod
    def set_serializer_object(model_serializer, data_dict):
        """
        Validate and save a dictionary to a model.
        :param model_serializer
        :param data_dict
        :return saved serialized object
        """
        print("Inside set_serializer_object")
        serializer = model_serializer(
            data=data_dict,
            partial=True
        )
        print("serializer", serializer)
        if serializer.is_valid(raise_exception=True):
            print("saved")
            return serializer.save()

    @staticmethod
    def update_serializer_object(previous_record, model_serializer, data_dict):
        """
        Validate and save a dictionary to a model.
        :param model_serializer
        :param data_dict
        :param previous_record
        :return saved serialized object
        """
        serializer = model_serializer(
            previous_record,
            data=data_dict,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            return serializer.save()

