import mysql.connector
from mysql.connector import errorcode
from _database import Database


class BaseRepository():
    """A class to represent the base repository which will be extended by entity repositories."""

    db: Database

    def __init__(self, database):
        self.db = database

    def report_error(self, error):
        print("SQL ERROR - Code:{}, Msg: '{}'".format(error.errno, error.msg))
