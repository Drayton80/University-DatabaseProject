import psycopg2
import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from model.Connection import Connection
from model.entities.User import User

from control.exceptions.RepeatedPrimaryKeyException import RepeatedPrimaryKeyException


class Follow:
    def __init_(self, follow_as_list):
        self.confirmation = follow_as_list[0]
        self.follower_user_name = follow_as_list[1]
        self.followed_user_name = follow_as_list[2]
        
    @classmethod
    def get_follow_instance(cls, follower, followed):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "select * from seguimento where nome_seguidor=%s and nome_seguido=%s",
            (follower.user_name, followed.user_name)
        )

        follows_as_lists = cursor.fetchall()

        if follows_as_lists:
            follow_relationship = Follow()
            follow_relationship.confirmation       = follows_as_lists[0][0]
            follow_relationship.follower_user_name = follows_as_lists[0][1]
            follow_relationship.followed_user_name = follows_as_lists[0][2]
        else:
            follow_relationship = None

        connection.close_database_connection()

        return follow_relationship

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

        entity_instance = Follow()
        entity_instance.confirmation       = confirmation
        entity_instance.follower_user_name = follower.user_name
        entity_instance.followed_user_name = followed.user_name

        return entity_instance

    @classmethod
    def delete_instance(cls, follower, followed):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "delete from seguimento where nome_seguidor=%s and nome_seguido=%s", 
            [follower.user_name, followed.user_name])

        connection.close_database_connection()

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

