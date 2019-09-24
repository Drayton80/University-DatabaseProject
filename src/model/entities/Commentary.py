import datetime
import psycopg2
import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join('../..')))

from model.Connection import Connection
from model.entities.Topic import Topic
from model.entities.Notification import Notification


class Commentary:
    def __init__(self, commentary_as_list):
        if commentary_as_list:
            self.commentary_id = commentary_as_list[0]
            self.post_id = commentary_as_list[1]
            self.author_id = commentary_as_list[2]
            self.date = commentary_as_list[3]
            self.text = commentary_as_list[4]
            

    def __str__(self): 
        if self.text:
            text = str(self.text)
        else:
            text = ''

        return ' @' + self.author_id + ' (' + str(self.date) + ')' + ': ' + '\n   ' + text
        

    def _create_markups_from_this_commentary(self):
        connection = Connection()
        cursor = connection.start_database_connection()

        for word in self.text.split(' '):
            if '@' in word:
                user_name = re.sub('[^0-9a-zA-Z_]+', '', word)

                cursor.execute(
                    "select * from perfil where nome_usuario=%s", 
                    [user_name])

                user_exist = True if cursor.fetchall() else False 

                if user_exist:
                    cursor.execute(
                        "select * from marcacao_comentario where nome_perfil=%s and id_comentario=%s", 
                        (user_name, self.commentary_id))

                    markup_already_exist = True if cursor.fetchall() else False

                    if not markup_already_exist:
                        cursor.execute(
                            "insert into marcacao_comentario(nome_perfil, id_comentario) values (%s, %s)",
                            (user_name, self.commentary_id))
                        connection._connection.commit()
                        Notification.create_instance(user_name, id_commentarymarkup_perfil=user_name, id_commentarymarkup_commentary=self.commentary_id)

        connection.close_database_connection()

    def _create_topics_from_this_commentary(self):
        connection = Connection()
        cursor = connection.start_database_connection()

        for word in self.text.split(' '):
            if '#' in word:
                word = re.sub('[^0-9a-zA-Z]+', '', word)

                date = datetime.datetime.now()

                if not Topic.topic_exist(word):
                    cursor.execute(
                        "insert into topico(nome) values (%s)",
                        [word])

                cursor.execute(
                    "insert into topico_comentario(data, id_topico, id_comentario) values (%s, %s, %s)",
                    (date, word, self.commentary_id))

        connection.close_database_connection()
    
    @classmethod
    def _date_correct_format(cls, date):
        if isinstance(date, datetime.datetime):
            return str(date.day) + '/' + str(date.month) + '/' + str(date.year)
        else:
            return date

    @classmethod
    def get_commentary_instance(cls, commentary_id):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "select * from comentario where id=%s",
            [commentary_id]
        )

        commentary_as_list = cursor.fetchall()[0]

        if commentary_as_list:
            commentary = Commentary(commentary_as_list)
        else:
            commentary = None

        connection.close_database_connection()

        return commentary

    # TODO checar se está funcionando corretamente
    @classmethod
    def get_commentary_from_topic(cls, topic_name):
        connection = Connection()
        cursor = connection.start_database_connection()
        
        cursor.execute(
            "select comentario.id, comentario.id_postagem, comentario.id_autor, comentario.data, comentario.texto from topico_comentario" \
            " inner join comentario on topico_comentario.id_comentario = comentario.id" \
            " where topico_comentario.id_topico=%s order by topico_comentario.data desc",
            [topic_name])

        commentaries_as_lists = cursor.fetchall()
        commentaries = []

        for commentary_as_list in commentaries_as_lists:
            commentaries.append(Commentary(commentary_as_list))

        connection.close_database_connection()

        return commentaries

    @classmethod
    def create_instance(cls, post, text, user_author):
        connection = Connection()
        cursor = connection.start_database_connection()

        date = datetime.datetime.now()

        cursor.execute(
            "insert into comentario(id_postagem, id_autor, data, texto) values (%s, %s, %s, %s) returning id",
            (post.post_id, user_author.user_name, date, text))

        commentary_id = cursor.fetchone()[0]

        connection.close_database_connection()

        entity_instance = Commentary([commentary_id, post.post_id, user_author.user_name, date, text])
        entity_instance._create_topics_from_this_commentary()
        entity_instance._create_markups_from_this_commentary()
        
        return entity_instance

    @classmethod
    def delete_instance(cls, commentary_id):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "delete from comentario where id=%s", 
            [commentary_id])

        connection.close_database_connection()