import psycopg2
import os
import sys

sys.path.append(os.path.abspath(os.path.join('../..')))

from model.Connection import Connection
from model.relationships.Follow import Follow


class User:
    def __init__(self, user_as_list):
        if user_as_list:
            self.user_name = user_as_list[0]
            self.complete_name = user_as_list[1]
            self.password = user_as_list[2]
            self.biography = user_as_list[3]
            self.privacy = user_as_list[4]

    def __str__(self):
        user_name = str(self.user_name)
        privacy = 'Privado' if self.privacy else 'Público'
        follower_number = str(len(Follow().get_user_followers(self)))

        return user_name + ' (Perfil ' + privacy + ')'

    @classmethod
    def search_users(cls, search_key, order_by=None):
        connection = Connection()
        cursor = connection.start_database_connection()

        order_by_followers = isinstance(order_by, str) and order_by.lower() == 'followers number'
        
        try:
            search_key = str(search_key)
            search_parameter = '%' + search_key + '%'
            
            cursor.execute("select * from perfil where nome_usuario like %s or nome_real like %s or biografia like %s", 
                           [search_parameter, search_parameter, search_parameter])
            users_as_list = cursor.fetchall()
            all_users_informations = []

            for user_as_list in users_as_list:
                user_information = {'object': User(user_as_list)}                       
                all_users_informations.append(user_information)

            connection.close_database_connection()

            if order_by_followers:
                for user_information in all_users_informations:
                    user_information['followers number'] = len(Follow().get_user_followers(user_information['object']))

                all_users_informations = sorted(all_users_informations, key= lambda k: k['followers number'], reverse=True)

            #for user_information in all_users_informations:
            #    print(user_information['object'], user_information['followers number'])
            #input()
            return [user_information['object'] for user_information in all_users_informations]

        except ValueError:
            connection.close_database_connection()
            raise ValueError

        except Exception:
            connection.close_database_connection()
            raise Exception

