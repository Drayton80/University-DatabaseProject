import psycopg2
import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from model.Connection import Connection

from control.exceptions.RepeatedPrimaryKeyException import RepeatedPrimaryKeyException


class Follow:
    def __init_(self, follow_as_list):
        self.confirmation = follow_as_list[0]
        self.follower_user_name = follow_as_list[1]
        self.followed_user_name = follow_as_list[2]
        

    @classmethod
    def create_instance(cls, follower, followed):
        connection = Connection()
        cursor = connection.start_database_connection()

        if cls.follow_exist(follower, followed):      
            raise RepeatedPrimaryKeyException()
        
        confirmation = True if not followed.privacy else False

        cursor.execute(
            "insert into seguimento(confirmacao, nome_seguidor, nome_seguido) values (%s, %s, %s)",
            (confirmation, follower.user_name, followed.user_name))

        connection.close_database_connection()

    @classmethod
    def delete_instance(cls, follower, followed):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "delete from seguimento where nome_seguidor=%s and nome_seguido=%s", 
            [follower.user_name, followed.user_name])

        connection.close_database_connection()

    @classmethod
    def get_user_followers(cls, user):
        connection = Connection()
        cursor = connection.start_database_connection()

        user_name = str(user.user_name)
        # TODO corrigir query para retornar os usuários como uma lista de User
        cursor.execute("select * from perfil where nome_usuario=(nome_seguidor from seguimento where nome_seguido=%s)", [user_name])
        followers = cursor.fetchall()

        connection.close_database_connection()
        
        return followers

    @classmethod
    def follow_exist(cls, follower, followed):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "select * from seguimento where nome_seguidor=%s and nome_seguido=%s", 
            [follower.user_name, followed.user_name])

        follow_exist = True if cursor.fetchall() else False 

        connection.close_database_connection()

        return follow_exist

