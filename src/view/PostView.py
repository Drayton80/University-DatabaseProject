import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from model.entities.Post import Post

from view.View import UserView
from view.InputField import InputField
from view.ViewPartition import ViewPartition
from view.List import List
from view.Dialog import Dialog
from view.CommentaryView import CommentaryView

class PostView(UserView):
    def run(self):
        displayed_user_posts = self.displayed_user.get_user_posts()
        selected_post_index = self._filter_selected_index(self._show_post_list(displayed_user_posts))
        
        while True:
            if self._is_empty_field(selected_post_index):
                return None
            
            elif self._is_value_a_number(selected_post_index) and ( 
                not self._is_out_of_bounds(selected_post_index, len(displayed_user_posts))):
                selected_option = self._show_selected_post(displayed_user_posts[selected_post_index])
                
                while True:
                    if selected_option == 'R':
                        break
                    elif selected_option == '1':
                        CommentaryView(self.logged_user, displayed_user=self.displayed_user, displayed_post=displayed_user_posts[selected_post_index]).run()
                        selected_option = self._show_selected_post(displayed_user_posts[selected_post_index])
                    elif self._displayed_user_is_logged_user()     and selected_option == '2':
                        Post.delete_instance(displayed_user_posts[selected_post_index].post_id)
                        displayed_user_posts = self.displayed_user.get_user_posts()
                        break
                    else:
                        selected_option = self._show_selected_post(displayed_user_posts[selected_post_index], information_message='Escolha Inválida')

                selected_post_index = self._filter_selected_index(self._show_post_list(displayed_user_posts))
            else:
                selected_post_index = self._filter_selected_index(self._show_post_list(displayed_user_posts , information_message='Escolha Inválida'))
                       
    def _show_post_list(self, post_list, information_message=None):
        ViewPartition().border_logo()
        
        if_list_is_empty_message = 'Você não possui Posts' if self._displayed_user_is_logged_user else 'Este usuário não possui Posts'

        List(post_list, if_list_is_empty_message=if_list_is_empty_message).run()

        ViewPartition().border_divisory()
               
        print('Caso deseje visualizar algum post, selecione ele pelo número ao lado')
        print("(Caso deseje retornar, deixe o campo em branco)")

        ViewPartition().border_information_message(information_message)

        return self._filter_selected_value(InputField().show('>>'))

    def _show_selected_post(self, post, information_message=None):
        ViewPartition().border_logo()
            
        print('@' + str(post.author_id) + ' - ' + str(post.date))

        ViewPartition().border_divisory()

        if post.image:
            Dialog().show_image(post.image)

        if not self._is_empty_field(post.text):
            print(str(post.text))
            ViewPartition().border_divisory()

        print("O que gostaria de fazer? Digite uma das opcoes abaixo:")
        print(" 1 - Ver Comentários")
        
        if self._displayed_user_is_logged_user():
            print(" 2 - Deletar esse Post")

        print(" R - Retornar para Lista de Posts")

        ViewPartition().border_information_message(information_message)

        return self._filter_selected_value(InputField().show('>>'))         