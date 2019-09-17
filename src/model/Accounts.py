import psycopg2
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from model.Connection import Connection
from model.entities.User import User
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
            user_as_list = cursor.fetchall()

            self.connection.close_database_connection()
            return User(user_as_list)

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
            user_as_list = cursor.fetchall()

            if user_as_list:
                user = User(user_as_list[0])
            else:
                user = None

            # Se a senha do usuário for diferente da senha digitada no campo:
            if user and user.password != password:
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
            user = User(None)
            user.complete_name = str(complete_name)
            user.user_name = str(user_name)
            user.password = str(password)
            user.biography = ""
            user.privacy = False

            cursor.execute("select * from perfil where nome_usuario=%s", [user.user_name])
            
            # Se existir algum usuário com o mesmo nome de usuário, lança exceção avisando isso
            if cursor.fetchall():
                raise RepeatedPrimaryKeyException()

            cursor.execute(
                "insert into perfil(nome_usuario, nome_real, senha, biografia, privacidade) values (%s, %s, %s, %s, %s)", 
                (user.user_name, user.complete_name, user.password, user.biography, user.privacy)
            )
            
            self.connection.close_database_connection()

            return user

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
            users_as_list = cursor.fetchall()
            users = []

            for user_as_list in users_as_list:
                users.append(User(user_as_list))

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

    