import psycopg2
import os
import sys
import traceback

sys.path.append(os.path.abspath(os.path.join('../..')))

from model.Connection import Connection
from model.entities.Post import Post
from model.entities.Commentary import Commentary
from model.entities.Notification import Notification

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
        #follower_number = str(len(self.get_user_followers()))

        return user_name + ' (Perfil ' + privacy + ')'
    
    def set_privacy(self, privacy: bool):
        connection = Connection()
        cursor = connection.start_database_connection()

        self.privacy = privacy

        cursor.execute(
            "update perfil set privacidade=%s where nome_usuario=%s",
            (privacy, self.user_name)
        )

        connection.close_database_connection()
    
    def get_user_followers(self):
        connection = Connection()
        cursor = connection.start_database_connection()

        user_name = str(self.user_name)
        
        cursor.execute(
            "select nome_usuario, nome_real, senha, biografia, privacidade" \
            " from seguimento inner join perfil on seguimento.nome_seguidor = perfil.nome_usuario " \
            " where nome_seguido=%s and confirmacao=%s", 
            (user_name, True))
            
        followers_as_list = cursor.fetchall()
        followers = []

        for follower_as_list in followers_as_list:
            followers.append(User(follower_as_list))

        connection.close_database_connection()
        
        return followers

    def get_user_followeds(self):
        connection = Connection()
        cursor = connection.start_database_connection()

        user_name = str(self.user_name)
        
        cursor.execute(
            "select nome_usuario, nome_real, senha, biografia, privacidade" \
            " from seguimento inner join perfil on seguimento.nome_seguido = perfil.nome_usuario " \
            " where nome_seguidor=%s and confirmacao=%s",
            (user_name, True))
            
        followeds_as_list = cursor.fetchall()
        followeds = []

        for followed_as_list in followeds_as_list:
            followeds.append(User(followed_as_list))

        connection.close_database_connection()
        
        return followeds

    def get_user_posts(self):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "select postagem.id, data, texto, foto, id_autor from postagem" \
            " left join seguimento on postagem.id_autor = seguimento.nome_seguido" \
            " where id_autor=%s or id_autor=seguimento.nome_seguido" \
            " order by data desc",
            [self.user_name]
        )

        posts_as_lists = cursor.fetchall()
        posts = []

        for post_as_list in posts_as_lists:
            posts.append(Post(post_as_list))

        connection.close_database_connection()

        return posts

    def get_user_notifications(self):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "select * from notificacao where id_perfil=%s order by data desc",
            [self.user_name]
        )

        notifications_as_lists = cursor.fetchall()
        notifications = []

        for notification_as_list in notifications_as_lists:
            notifications.append(Notification(notification_as_list))

        connection.close_database_connection()

        return notifications

    @classmethod
    def get_user_instance(cls, user_name):
        connection = Connection()
        cursor = connection.start_database_connection()

        cursor.execute(
            "select * from perfil where nome_usuario=%s",
            [user_name]
        )

        user_as_list = cursor.fetchall()[0]

        if user_as_list:
            user = User(user_as_list)
        else:
            user = None

        connection.close_database_connection()

        return user

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
                    user_information['followers number'] = len(user_information['object'].get_user_followers())

                all_users_informations = sorted(all_users_informations, key= lambda k: k['followers number'], reverse=True)

            return [user_information['object'] for user_information in all_users_informations]

        except ValueError:
            connection.close_database_connection()
            raise ValueError

        except Exception as e:
            connection.close_database_connection()
            traceback.print_exc()
            raise Exception

