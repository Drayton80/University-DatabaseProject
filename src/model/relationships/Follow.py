import psycopg2
import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from model.Connection import Connection
from model.entities.User import User
from model.entities.Notification import Notification

from control.exceptions.RepeatedPrimaryKeyException import RepeatedPrimaryKeyException


class Follow:
    def __init__(self, follow_as_list):
        self.confirmation = follow_as_list[0]
        self.follower_user_name = follow_as_list[1]
        self.followed_user_name = follow_as_list[2]
    
    def set_confirmation(self, confirmation: bool):
        connection = Connection()
        cursor = connection.start_database_connection()

        self.confirmation = confirmation

        cursor.execute(
            "update seguimento set confirmacao=%s where nome_seguidor=%s and nome_seguido=%s",
            (confirmation, self.follower_user_name, self.followed_user_name)
        )

        connection.close_database_connection()

        Notification.create_instance(self.follower_user_name, 
                                     notification_type='follow confirmation',
                                     id_follow_follower=self.follower_user_name, 
                                     id_follow_followed=self.followed_user_name)

    @classmethod
    def get_follow_instance(cls, follower_id, followed_id):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "select * from seguimento where nome_seguidor=%s and nome_seguido=%s",
            (follower_id, followed_id)
        )

        follow_as_list = cursor.fetchall()[0]

        if follow_as_list:
            follow_relationship = Follow(follow_as_list)
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

        Notification.create_instance(followed.user_name, id_follow_follower=follower.user_name, id_follow_followed=followed.user_name)

        entity_instance = Follow([confirmation, follower.user_name, followed.user_name])

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

