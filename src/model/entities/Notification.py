import datetime
import psycopg2
import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join('../..')))

from model.Connection import Connection


class Notification:
    def __init__(self, notification_as_list):
        if notification_as_list:
            self.notification_id = notification_as_list[0]
            self.date = self._date_correct_format(notification_as_list[1])
            self.notification_type = notification_as_list[2]

            self.id_user = notification_as_list[3]

            self.id_follow_follower = notification_as_list[4]
            self.id_follow_followed = notification_as_list[5]

            self.id_postmarkup_perfil = notification_as_list[6]
            self.id_postmarkup_post = notification_as_list[7]

            self.id_commentarymarkup_perfil = notification_as_list[8]
            self.id_commentarymarkup_commentary = notification_as_list[9]

    def __str__(self):
        connection = Connection()
        cursor = connection.start_database_connection()
        
        if self.notification_type == 'follow':
            title = 'Notificação de Seguimento (' + self.date + ')\n'

            cursor.execute("select privacidade from perfil where nome_usuario=%s", [self.id_user])
            user_privacy = cursor.fetchone()[0]
            
            if user_privacy:
                text = 'O Usuário @' + self.id_follow_follower + ' gostaria de te seguir'
            else:
                text = 'O Usuário @' + self.id_follow_follower + ' começou a te seguir'

        elif self.notification_type == 'follow confirmation':
            title = 'Notificação de Seguimento (' + self.date + ')\n'

            cursor.execute(
                "select * from seguimento where nome_seguidor=%s and nome_seguido=%s",
                (self.id_follow_follower, self.id_follow_followed))

            follow_as_list = cursor.fetchall()

            if follow_as_list:
                confirmation = follow_as_list[0][0]

                if confirmation == True:
                    text = 'O Usuário @' + self.id_follow_followed + ' aceitou seu pedido'
                else:
                    text = 'O Usuário @' + self.id_follow_followed + ' negou seu pedido'
            else:
                text = ''

        elif self.notification_type == 'post markup':
            title = 'Notificação de Marcação (' + self.date + ')\n'

            cursor.execute("select id_autor from postagem where id=%s", [self.id_postmarkup_post])
            post_owner = cursor.fetchone()[0]

            text = 'O Usuário @' + post_owner + ' te marcou em um Post dele'

        elif self.notification_type == 'commentary markup':
            title = 'Notificação de Marcação (' + self.date + ')\n'

            cursor.execute("select id_postagem, id_autor from comentario where id=%s", [self.id_commentarymarkup_commentary])
            post_information = cursor.fetchall()[0]
            post_id_that_commentary_belongs = post_information[0]
            commentary_owner = post_information[1]
            cursor.execute("select id_autor from postagem where id=%s", [post_id_that_commentary_belongs])
            post_owner = cursor.fetchone()[0]

            text = 'O Usuário @' + commentary_owner + ' te marcou em um Post de @' + post_owner

        else:
            title = ''
            text = ''

        connection.close_database_connection()

        return title + '   ' + text

    @classmethod
    def _date_correct_format(cls, date):
        if isinstance(date, datetime.datetime):
            return str(date.day) + '/' + str(date.month) + '/' + str(date.year)
        else:
            return date

    @classmethod
    def create_instance(cls, user_id, notification_type=None,
                        id_follow_follower=None, id_follow_followed=None,
                        id_postmarkup_perfil=None, id_postmarkup_post=None,
                        id_commentarymarkup_perfil=None, id_commentarymarkup_commentary=None):

        connection = Connection()
        cursor = connection.start_database_connection()

        date = datetime.datetime.now()

        if not notification_type:
            if id_follow_follower and id_follow_followed:
                notification_type = 'follow'
            elif id_postmarkup_perfil and id_postmarkup_post:
                notification_type = 'post markup'
            elif id_commentarymarkup_perfil and id_commentarymarkup_commentary:
                notification_type = 'commentary markup'
            else:
                notification_type = 'anomaly' 

        cursor.execute(
            "insert into notificacao(data, tipo, id_perfil, id_seguimento_seguidor, id_seguimento_seguido, id_marcacao_postagem_perfil," \
            " id_marcacao_postagem_idpostagem, id_marcacao_comentario_perfil, id_marcacao_comentario_idcomentario) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) returning id",
            (date, notification_type, user_id, id_follow_follower, id_follow_followed, id_postmarkup_perfil, id_postmarkup_post,
            id_commentarymarkup_perfil, id_commentarymarkup_commentary))

        notification_id = cursor.fetchone()[0]

        connection.close_database_connection()

        entity_instance = Notification([notification_id, date, notification_type, user_id, 
                                        id_follow_follower, id_follow_followed, 
                                        id_postmarkup_perfil, id_postmarkup_post,
                                        id_commentarymarkup_perfil, id_commentarymarkup_commentary])
        
        return entity_instance

    @classmethod
    def delete_instance(cls, notification_id):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "delete from notificacao where id=%s", 
            [notification_id])

        connection.close_database_connection()
