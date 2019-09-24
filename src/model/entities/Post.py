import datetime
import psycopg2
import re
import os
import sys
from PIL import Image
from io import BytesIO

sys.path.append(os.path.abspath(os.path.join('../..')))

from model.Connection import Connection
from model.entities.Topic import Topic
from model.entities.Commentary import Commentary
from model.entities.Notification import Notification


class Post:
    def __init__(self, post_as_list):
        if post_as_list:
            self.post_id = post_as_list[0]
            self.date = self._date_correct_format(post_as_list[1]) 
            self.text = post_as_list[2]
            self.image = self._image_from_image_bytes(post_as_list[3])
            self.author_id = post_as_list[4]

    def __str__(self):        
        fragment_index_limit = 16

        if isinstance(self.text, str) and len(self.text) > fragment_index_limit:
            text_fragment = self.text[:fragment_index_limit] + '[...]'
        else:
            text_fragment = self.text 

        return self.author_id + ' (' + str(self.date) + ')' + ': ' + str(text_fragment)

    def get_post_commentaries(self):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "select * from comentario where id_postagem=%s" \
            " order by data desc",
            [self.post_id]
        )

        commentaries_as_lists = cursor.fetchall()
        commentaries = []

        for commentary_as_list in commentaries_as_lists:
            commentaries.append(Commentary(commentary_as_list))

        connection.close_database_connection()

        return commentaries        

    def _create_markups_from_this_post(self):
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
                        "select * from marcacao_postagem where nome_perfil=%s and id_postagem=%s", 
                        (user_name, self.post_id))

                    markup_already_exist = True if cursor.fetchall() else False

                    if not markup_already_exist:
                        cursor.execute(
                            "insert into marcacao_postagem(nome_perfil, id_postagem) values (%s, %s)",
                            (user_name, self.post_id))
                        
                        connection._connection.commit()
                        Notification.create_instance(user_name, id_postmarkup_perfil=user_name, id_postmarkup_post=self.post_id)

        connection.close_database_connection()

    def _create_topics_from_this_post(self):
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
                    "insert into topico_postagem(data, id_topico, id_postagem) values (%s, %s, %s)",
                    (date, word, self.post_id))

        connection.close_database_connection()
    
    @classmethod
    def _date_correct_format(cls, date):
        if isinstance(date, datetime.date):
            return str(date.day) + '/' + str(date.month) + '/' + str(date.year)
        else:
            return date

    @classmethod
    def _image_from_image_bytes(cls, image_bytes):
        return Image.open(BytesIO(image_bytes)) if image_bytes else None
    
    @classmethod
    def _image_bytes_from_path(cls, image_path):
        if image_path:
            with open(image_path, 'rb') as image_file:
                return image_file.read()
        else:
            return None

    # TODO checar se está funcionando corretamente
    @classmethod
    def get_posts_from_topic(cls, topic_name):
        connection = Connection()
        cursor = connection.start_database_connection()
        
        cursor.execute(
            "select id, postagem.data, texto, foto, id_autor from topico_postagem" \
            " inner join postagem on topico_postagem.id_postagem = postagem.id "   \
            " inner join topico on topico_postagem.id_topico = topico.nome"        \
            " where topico.nome=%s order by case"                                  \
            " when isdate(topico_postagem.data)=1 then convert(datetime, topico_postagem.data, 101) desc",
            [topic_name])

        posts_as_lists = cursor.fetchall()
        posts = []

        for post_as_list in posts_as_lists:
            posts.append(Post(post_as_list))

        connection.close_database_connection()

        return posts

    @classmethod
    def get_post_instance(cls, post_id):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "select * from postagem where id=%s",
            [post_id]
        )

        post_as_list = cursor.fetchall()[0]

        if post_as_list:
            post = Post(post_as_list)
        else:
            post = None

        connection.close_database_connection()

        return post

    @classmethod
    def create_instance(cls, text, image_path, user_author):
        connection = Connection()
        cursor = connection.start_database_connection()

        date = datetime.datetime.now()
        image_bytes = cls._image_bytes_from_path(image_path)

        cursor.execute(
            "insert into postagem(data, texto, foto, id_autor) values (%s, %s, %s, %s) returning id",
            (date, text, image_bytes, user_author.user_name))

        post_id = cursor.fetchone()[0]

        connection.close_database_connection()

        entity_instance = Post([post_id, date, text, image_bytes, user_author.user_name])
        entity_instance._create_topics_from_this_post()
        entity_instance._create_markups_from_this_post()
        
        return entity_instance

    @classmethod
    def delete_instance(cls, post_id):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "delete from postagem where id=%s", 
            [post_id])

        connection.close_database_connection()
