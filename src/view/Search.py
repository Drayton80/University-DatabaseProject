import os
import sys
import datetime

sys.path.append(os.path.abspath(os.path.join('..')))

from model.entities.User import User
from model.entities.Post import Post
from model.entities.Commentary import Commentary

from view.View import UserView
from view.List import List
from view.InputField import InputField
from view.ViewPartition import ViewPartition


class SearchUser(UserView):    
    def run(self):
        search_key = self.show()

        if super()._is_empty_field(search_key):
            return None

        users_list = User.search_users(search_key, order_by='followers number')

        wrong_selection_message = None

        while(True):
            selected_index = self._filter_selected_index(self.show(users_list=users_list, information_message=wrong_selection_message))

            if self._is_empty_field(selected_index):
                return None
            elif not self._is_out_of_bounds(selected_index, len(users_list)):
                return users_list[selected_index] 
            else:
                wrong_selection_message = 'Opção inválida'     

    def show(self, users_list=[], information_message=None):
        ViewPartition().border_logo()
        
        if not users_list:
            print("Para pesquisar determinado usuário, basta digitar seu nome abaixo")      
        else:
            print("Sua pesquisa resultou em", len(users_list), "usuários:")
            List(users_list).run()

            ViewPartition().border_divisory()
            print("Selecione o usuário que você deseja visualizar pelo número ao lado")

        print("(Caso deseje retornar, deixe o campo em branco)")
        
        ViewPartition().border_information_message(information_message)

        return InputField().show('>>')


class SearchTopic(UserView):
    def run(self):
        search_key = self.show()

        if self._is_empty_field(search_key):
            return None

        posts = Post.get_posts_from_topic(search_key)
        posts = posts if isinstance(posts, list) else []
        commentaries = Commentary.get_commentary_from_topic(search_key)
        commentaries = commentaries if isinstance(commentaries, list) else []

        topic_list = posts + commentaries

        if topic_list:
            topic_list = sorted(topic_list, key=lambda x: x.date, reverse=True)

        wrong_selection_message = None

        while(True):
            selected_index = self._filter_selected_index(self.show(topic_list=topic_list, information_message=wrong_selection_message))

            if self._is_empty_field(selected_index):
                return None
            elif isinstance(selected_index, int) and not self._is_out_of_bounds(selected_index, len(topic_list)):
                return_object = topic_list[selected_index] 
                
                if isinstance(return_object, Post):
                    return return_object
                elif isinstance(return_object, Commentary):
                    return Post.get_post_instance(return_object.post_id)
            else:
                wrong_selection_message = 'Opção inválida'

    def show(self, topic_list=[], information_message=None):
        ViewPartition().border_logo()
        
        if not topic_list:
            print("Para pesquisar determinado tópico, basta digitar uma palavra abaixo")      
        else:
            print("Sua pesquisa resultou em", len(topic_list), "tópicos:")
            List(topic_list, separator='\n').run()

            ViewPartition().border_divisory()
            print("Selecione o tópico que você deseja visualizar pelo número ao lado")

        print("(Caso deseje retornar, deixe o campo em branco)")
        
        ViewPartition().border_information_message(information_message)

        return InputField().show('>>')
            
            
        