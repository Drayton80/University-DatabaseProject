import psycopg2
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from model.Connection import Connection
from control.Validator import Validator
from control.exceptions.WrongPasswordException import WrongPasswordException
from control.exceptions.RepeatedPrimaryKeyException import RepeatedPrimaryKeyException

class Accounts:
    connection = Connection()

    def update_user(self, user_name, complete_name, password, biography, privacy):
        pass

    def get_user(self, user_name):
        cursor = self.connection.start_database_connection()
        
        try:
            user_name = str(user_name)
            
            cursor.execute("select * from perfil where nome_usuario=%s", [user_name])
            user = cursor.fetchall()

            self.connection.close_database_connection()
            return user

        except ValueError:
            self.connection.close_database_connection()
            raise ValueError

        except WrongPasswordException:
            self.connection.close_database_connection()
            raise WrongPasswordException

        except Exception:
            self.connection.close_database_connection()
            raise Exception

    def login_user(self, user_name, password):
        cursor = self.connection.start_database_connection()
        
        try:
            user_name = str(user_name)
            password = str(password)
            
            cursor.execute("select * from perfil where nome_usuario=%s", [user_name])
            user = cursor.fetchall()

            # Se a senha do usuário for diferente da senha digitada no campo:
            if user and user[0][2] != password:
                raise WrongPasswordException()

            self.connection.close_database_connection()
            return user

        except ValueError:
            self.connection.close_database_connection()
            raise ValueError

        except WrongPasswordException:
            self.connection.close_database_connection()
            raise WrongPasswordException

        except Exception:
            self.connection.close_database_connection()
            raise Exception
    

    def register_user(self, user_name, complete_name, password):
        cursor = self.connection.start_database_connection()
        
        try:
            complete_name = str(complete_name)
            user_name = str(user_name)
            password = str(password)
            biography = ""
            privacy = False
            
            cursor.execute("select * from perfil where nome_usuario=%s", [user_name])
            
            # Se existir algum usuário com o mesmo nome de usuário, lança exceção avisando isso
            if cursor.fetchall():
                raise RepeatedPrimaryKeyException()

            cursor.execute(
                "insert into perfil(nome_usuario, nome_real, senha, biografia, privacidade) values (%s, %s, %s, %s, %s)", 
                (user_name, complete_name, password, biography, privacy)
            )
            
            self.connection.close_database_connection()

            return [(user_name, complete_name, password, biography, privacy)]

        except RepeatedPrimaryKeyException:
            self.connection.close_database_connection()
            raise RepeatedPrimaryKeyException

        except Exception:
            self.connection.close_database_connection()
            raise Exception

    def search_users(self, user_name_fragment):
        cursor = self.connection.start_database_connection()
        
        try:
            user_name_fragment = str(user_name_fragment)
            search_parameter = '%' + user_name_fragment + '%'
            
            cursor.execute("select * from perfil where nome_usuario like %s", [search_parameter])
            users = cursor.fetchall()

            self.connection.close_database_connection()
            return users

        except ValueError:
            self.connection.close_database_connection()
            raise ValueError

        except WrongPasswordException:
            self.connection.close_database_connection()
            raise WrongPasswordException

        except Exception:
            self.connection.close_database_connection()
            raise Exception

    