import json
import cx_Oracle
from pandas import DataFrame
import os

class OracleQueries:

    def __init__(self, can_write:bool=False):
        self.can_write = can_write
        self.host = "localhost"
        self.port = 1521
        self.service_name = 'XEPDB1'
        self.sid = 'XE'

        # --- CORREÇÃO DE CAMINHO ---
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Procura em src/conexion/passphrase/authentication.oracle
        file_path = os.path.join(base_path, "passphrase", "authentication.oracle")
        
        if not os.path.exists(file_path):
            # Fallback para src/passphrase
             file_path = os.path.join(base_path, "..", "passphrase", "authentication.oracle")

        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.user, self.passwd = f.read().strip().split(',')
        else:
             # Valores padrão caso não encontre o arquivo (evita crash na importação)
             self.user, self.passwd = "system", "oracle" 

    def __del__(self):
        if hasattr(self, "cur"):
            self.close()

    def connectionString(self, in_container:bool=False):
        if not in_container:
            string_connection = cx_Oracle.makedsn(host=self.host, port=self.port, sid=self.sid)
        elif in_container:
            string_connection = cx_Oracle.makedsn(host=self.host, port=self.port, service_name=self.service_name)
        return string_connection

    def connect(self):
        self.conn = cx_Oracle.connect(user=self.user, password=self.passwd, dsn=self.connectionString())
        self.cur = self.conn.cursor()
        return self.cur

    def sqlToDataFrame(self, query:str) -> DataFrame:
        self.cur.execute(query)
        rows = self.cur.fetchall()
        # Tratamento para caso a query não retorne nada
        if self.cur.description:
             return DataFrame(rows, columns=[col[0].lower() for col in self.cur.description])
        return DataFrame()

    def write(self, query:str):
        if not self.can_write:
            raise Exception('Can\'t write using this connection')
        self.cur.execute(query)
        self.conn.commit()

    def close(self):
        if self.cur:
            self.cur.close()

    def executeDDL(self, query:str):
        self.cur.execute(query)