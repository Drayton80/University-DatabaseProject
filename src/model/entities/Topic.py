import datetime
import psycopg2
import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from model.Connection import Connection

from control.exceptions.RepeatedPrimaryKeyException import RepeatedPrimaryKeyException


class Topic:
    def __init_(self, topic_as_list):
        self.name = topic_as_list[0]
    
    @classmethod
    def get_topic_instance(cls, name):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "select * from topico where nome=%s",
            [name]
        )

        topics_as_lists = cursor.fetchall()

        if topics_as_lists:
            topic = Topic()
            topic.name = name
        else:
            topic = None

        connection.close_database_connection()

        return topic

    @classmethod
    def create_instance(cls, name):
        connection = Connection()
        cursor = connection.start_database_connection()

        if cls.topic_exist(name):      
            raise RepeatedPrimaryKeyException()

        cursor.execute(
            "insert into topico(nome) values (%s)",
            [name])

        connection.close_database_connection()

        entity_instance = Topic()
        entity_instance.name = name

        return entity_instance

    @classmethod
    def topic_exist(cls, name):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "select * from topico where nome=%s", 
            [name])

        topic_exist = True if cursor.fetchall() else False 

        connection.close_database_connection()

        return topic_exist