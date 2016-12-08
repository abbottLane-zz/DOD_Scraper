import os
import pyodbc
import traceback

import configparser


class DBAccess():
    def __init__(self, db_config_name):
        self.db_env = db_config_name
        self.config_path = "dbaccessconfig.ini"
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)
        self.host = self.config[self.db_env]["host"]
        self.odbc_driver = self.config[self.db_env]["driver"]
        self.port = self.config[self.db_env]["port"]
        self.database = self.config[self.db_env]["database"]
        self.user = self.config[self.db_env]["user"]
        self.password = self.config[self.db_env]["password"]

        self.connStr ='DRIVER={'+self.odbc_driver\
                      +'};DATABASE='+self.database\
                      +';UID='+self.user\
                      +';PWD='+self.password\
                      +';SERVER='+self.host\
                      +';PORT='+self.port\
                      +';'

        print "Connecting with params: " + self.connStr
        try:
            self.conn = pyodbc.connect(self.connStr)
        except Exception:
            self.conn = None
            print "Connection problem occured: Could not connect to host:" + self.host

    def execute_INSERT_INTO_query(self, query):
        if self.conn:
            try:
                self.conn.cursor().execute(query)
                self.conn.commit()
            except Exception:
                traceback.print_exc()
                print "ProblemQuery:  " + query