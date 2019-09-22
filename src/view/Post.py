import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from model.entities.User import User

from view.View import UserView
from view.InputField import InputField
from view.ViewPartition import ViewPartition
from view.List import List

class Post(UserView):
    def run(self):
        displayed_user_posts = self.displayed_user.get_user_posts()

        selected_option = self._show_post_list(displayed_user_posts)

        while True:
            break
                       
    def _show_post_list(self, post_list):
        if_list_is_empty_message = 'Você não possui Posts' if self._displayed_user_is_logged_user else 'Este usuário não possui Posts'

        List(post_list, if_list_is_empty_message=if_list_is_empty_message).run()

        return InputField().show('>>')

    def _show_selected_post(self, post, information_message=None):
        ViewPartition().border_logo()
            
        print()

        ViewPartition().border_information_message(information_message)

        return InputField().show('>>')
            

    def selection(self, selected_option):
        pass