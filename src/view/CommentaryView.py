import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from model.entities.Commentary import Commentary

from view.View import UserView
from view.InputField import InputField
from view.ViewPartition import ViewPartition
from view.Create import CommentaryCreate
from view.List import List
from view.Dialog import Dialog

class CommentaryView(UserView):
    def run(self):
        displayed_post_commentaries = self.displayed_post.get_post_commentaries()
        selected_commentary_index = self._filter_selected_index(self._show_commentary_list(displayed_post_commentaries))
        
        while True:
            if self._is_empty_field(selected_commentary_index):
                return None

            elif isinstance(selected_commentary_index, str) and selected_commentary_index.upper() == 'C':
                CommentaryCreate(self.logged_user, displayed_user=self.displayed_user, displayed_post=self.displayed_post).run()
                displayed_post_commentaries = self.displayed_post.get_post_commentaries()
                selected_commentary_index = self._filter_selected_index(self._show_commentary_list(displayed_post_commentaries))
            
            elif self._is_value_a_number(selected_commentary_index) and ( 
                not self._is_out_of_bounds(selected_commentary_index, len(displayed_post_commentaries))):
                selected_option = self._show_selected_commentary(displayed_post_commentaries[selected_commentary_index])
                
                while True:
                    if selected_option == 'R' or self._is_empty_field(selected_option):
                        break
                    elif self._post_belongs_to_logged_user() and selected_option == '1':
                        Commentary.delete_instance(displayed_post_commentaries[selected_commentary_index].commentary_id)
                        displayed_post_commentaries = self.displayed_post.get_post_commentaries()
                        break
                    else:
                        selected_option = self._show_selected_commentary(displayed_post_commentaries[selected_commentary_index], information_message='Escolha Inválida')

                selected_commentary_index = self._filter_selected_index(self._show_commentary_list(displayed_post_commentaries))
            else:
                selected_commentary_index = self._filter_selected_index(self._show_commentary_list(displayed_post_commentaries , information_message='Escolha Inválida'))
                       
    def _show_commentary_list(self, commentary_list, information_message=None):
        ViewPartition().border_logo()
        print(self.displayed_post)
        ViewPartition().border_divisory()
        
        if_list_is_empty_message = 'Este Post não possui Comentários'

        if commentary_list:
            print("Todos os Comentários:\n")

        List(commentary_list, 
            if_list_is_empty_message=if_list_is_empty_message, 
            separator='\n', index_left_list_element=False, word_before_index='Comentário ').run()

        ViewPartition().border_divisory()
               
        print('Caso deseje visualizar algum comentário, selecione ele pelo número ao acima dele')
        print('Caso deseje escrever um novo comentário digite \'C\' e pressione Enter')
        print("(Caso deseje retornar, deixe o campo em branco)")

        ViewPartition().border_information_message(information_message)

        return self._filter_selected_value(InputField().show('>>'))

    def _show_selected_commentary(self, commentary, information_message=None):
        ViewPartition().border_logo()
        print(self.displayed_post)
        ViewPartition().border_divisory()            
        print(commentary)
        ViewPartition().border_divisory()

        print("O que gostaria de fazer? Digite uma das opcoes abaixo:")
        
        if self._post_belongs_to_logged_user():
            print(" 1 - Deletar esse Comentário")

        print(" R - Retornar para Lista de Comentários")

        ViewPartition().border_information_message(information_message)

        return self._filter_selected_value(InputField().show('>>'))       