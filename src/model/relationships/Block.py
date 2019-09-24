import psycopg2
import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))

from model.Connection import Connection

from control.exceptions.RepeatedPrimaryKeyException import RepeatedPrimaryKeyException


class Block:
    def __init__(self, follow_as_list):
        self.blocker_user_name = follow_as_list[0]
        self.blocked_user_name = follow_as_list[1]
    

    @classmethod
    def get_block_instance(cls, blocker_user_name, blocked_user_name):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "select * from bloqueio where nome_bloqueador=%s and nome_bloqueado=%s",
            (blocker_user_name, blocked_user_name)
        )

        block_as_list = cursor.fetchall()[0]

        if block_as_list:
            block_relationship = Block(block_as_list)
        else:
            block_relationship = None

        connection.close_database_connection()

        return block_relationship

    @classmethod
    def create_instance(cls, blocker_user_name, blocked_user_name):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "insert into bloqueio(nome_bloqueador, nome_bloqueado) values (%s, %s)",
            (blocker_user_name, blocked_user_name))

        entity_instance = Block([blocker_user_name, blocked_user_name])

        cursor.execute(
            "delete from comentario where id_autor=%s and comentario.id_postagem in" \
            " (select id from postagem where postagem.id_autor=%s)", 
            (blocker_user_name, blocked_user_name))

        cursor.execute(
            "delete from comentario where id_autor=%s and comentario.id_postagem in" \
            " (select id from postagem where postagem.id_autor=%s)", 
            (blocked_user_name, blocker_user_name))

        cursor.execute(
            "delete from seguimento where nome_seguidor=%s and nome_seguido=%s", 
            (blocker_user_name, blocked_user_name))

        cursor.execute(
            "delete from seguimento where nome_seguidor=%s and nome_seguido=%s", 
            (blocked_user_name, blocker_user_name))

        connection.close_database_connection()

        return entity_instance

    @classmethod
    def delete_instance(cls, blocker_user_name, blocked_user_name):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "delete from bloqueio where nome_bloqueador=%s and nome_bloqueado=%s", 
            (blocker_user_name, blocked_user_name))

        connection.close_database_connection()

    @classmethod
    def block_exist(cls, blocker_user_name, blocked_user_name):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "select * from bloqueio where nome_bloqueador=%s and nome_bloqueado=%s",
            (blocker_user_name, blocked_user_name)
        )

        block_exist = True if cursor.fetchall() else False 

        connection.close_database_connection()

        return block_exist

