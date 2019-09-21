import psycopg2
import os
import sys

sys.path.append(os.path.abspath(os.path.join('../..')))

from model.Connection import Connection


class Post:
    def __init_(self, post_as_list):
        if post_as_list:
            self.post_id = post_as_list[0]
            self.date = post_as_list[1]
            self.text = post_as_list[2]
            self.image = post_as_list[3]
            self.author_id = post_as_list[4]

    @classmethod
    def create_instance(cls, date, text, image, user_author):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "insert into postagem(data, texto, foto, id_autor) values (%s, %s, %s, %s)",
            (date, text, image, user_author.user_name))

        # TODO checar se insert retorna a tabela inserida, pq preciso do ID correto do post criado
        # TODO ver um jeito de obter o ID do post recem inserido

        connection.close_database_connection()

        entity_instance = Post()
        entity_instance.date      = date
        entity_instance.text      = text
        entity_instance.image     = image
        entity_instance.post_id   = None
        entity_instance.author_id = user_author.user_name
        
        return entity_instance
