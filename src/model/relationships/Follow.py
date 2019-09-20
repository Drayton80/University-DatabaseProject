import psycopg2
import os
import sys

sys.path.append(os.path.abspath(os.path.join('../..')))

from model.Connection import Connection
from model.entities.User import User

class Follow:
    def __init_(self, follow_as_list):
        self.confirmation = follow_as_list[0]
        self.follower_user_name = follow_as_list[1]
        self.followed_user_name = follow_as_list[2]
        

    @classmethod
    def get_user_followers(cls, user: User):
        cursor = Connection().start_database_connection()

        user_name = str(user.user_name)
            
        cursor.execute("select nome_seguidor from seguimento where nome_seguido=%s", [user_name])
        followers = cursor.fetchall()

        Connection().close_database_connection()
        
        return followers

