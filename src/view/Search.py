import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from model.entities.User import User

from view.List import List
from view.InputField import InputField
from view.ViewPartition import ViewPartition


class Search:
    def _is_empty_field(self, field_value):
        if field_value.isspace() or field_value in [None, '']:
            return True
        else:
            return False

    def _is_out_of_bounds(self, index, upper_limit):
        if index.isdigit() and 0 <= int(index)-1 < upper_limit:
            return False
        else:
            return True


class SearchUser(Search):
    def __init__(self, logged_user):
        self.logged_user = logged_user
    
    def run(self):
        search_key = self.show()

        if self._is_empty_field(search_key):
            return None

        users_list = User.search_users(search_key, order_by='followers number')

        wrong_selection_message = None

        while(True):
            selected_user_index = self.show(users_list=users_list, information_message=wrong_selection_message)

            if self._is_empty_field(selected_user_index):
                return None
            elif not self._is_out_of_bounds(selected_user_index, len(users_list)):
                return users_list[int(selected_user_index)-1] 
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

    def selection(self, search_key):
        return 
            
            
        