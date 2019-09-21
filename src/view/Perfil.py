import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from model.relationships.Follow import Follow
from model.entities.User import User

from view.InputField import InputField
from view.ViewPartition import ViewPartition
from view.Menus import Menus
from view.List import List
from view.Search import SearchUser

class Perfil:
      def __init__(self, logged_user):
            self.logged_user = logged_user

      def _empty_field(self, field_value):
        if field_value.isspace() or field_value in [None, '']:
            return True
        else:
            return False

      def _is_out_of_bounds(self, index, upper_limit):
        if index.isdigit() and 0 <= int(index)-1 < upper_limit:
            return False
        else:
            return True

      def run(self):
            selected_option = self.show(self.logged_user)
            returned_information  = self.selection(selected_option, self.logged_user)

            while True:
                  if isinstance(returned_information, dict) and 'command' in returned_information.keys():
                        command_is_string = isinstance(returned_information['command'], str)
                  else:
                        command_is_string = False

                  if   command_is_string and returned_information['command'] == 'home_logged_perfil':
                        return 'home_logged_perfil'

                  elif command_is_string and returned_information['command'] == 'outside_account':
                        return 'outside_account'

                  elif command_is_string and returned_information['command'] == 'show_another_perfil':
                        selected_option = self.show(returned_information['object'])
                        returned_information = self.selection(selected_option, returned_information['object'])

                  elif command_is_string and returned_information['command'] == 'wrong_selection':
                        selected_option = self.show(returned_information['object'], information_message=returned_information['information message'])
                        returned_information = self.selection(selected_option, returned_information['object'])

                  else:
                        selected_option = self.show(self.logged_user)
                        returned_information = self.selection(selected_option, self.logged_user)                 
                        

      def show(self, perfil_user, information_message=None):
            ViewPartition().border_logo()
            
            if not perfil_user:
                  return {'command': 'home_logged_perfil', 'object': None} 

            perfil_belongs_to_logged_user = True if self.logged_user.user_name == perfil_user.user_name else False

            if  perfil_belongs_to_logged_user:
                  print("Bem-vindo,", perfil_user.user_name)
                  ViewPartition().border_divisory()

            privacy_status = 'Privado' if perfil_user.privacy else 'Público'

            print("Informações do Perfil " + privacy_status            )   
            print("Nome de Usuário: " + str(perfil_user.user_name)     + "\n" \
                  "Nome Real: "       + str(perfil_user.complete_name) + "\n" \
                  "Biografia: "       + str(perfil_user.biography)     + "  " )
            
            ViewPartition().border_divisory()
            
            print("O que gostaria de fazer? Digite uma das opcoes abaixo:")
            
            # TODO checar se o usuário é seguidor do perfil_user para ver se isso será exibido:
            if not perfil_user.privacy or (perfil_user.privacy and True):
                  print(" 1 - Ver Postagens         \n" \
                        " 2 - Ver Seguidores        \n" \
                        " 3 - Ver Aqueles que Segue   " )
            
            if perfil_belongs_to_logged_user:
                  options_search      = " 4 - Buscar Perfil     \n" \
                                        " 5 - Buscar Tópico     \n" 
                  option_notificacoes = " N - Para Notificações \n"
                  option_deslogar     = " D - Para sair da Conta  "
                  extra_options = options_search + option_notificacoes + option_deslogar
            else:
                  option_seguir   = ' S - Para deixar de Seguir\n'if Follow().follow_exist(self.logged_user, perfil_user) else ' S - Para Seguir\n' 
                  option_bloquear = ' B - Para Bloquear\n' 
                  option_retornar = ' R - Para retornar para seu Perfil' 
                  extra_options = option_seguir + option_bloquear + option_retornar

            print(extra_options)

            ViewPartition().border_information_message(information_message)

            return InputField().show('>>')
            
      def _show_followers_list(self, followers_list):
            ViewPartition().border_logo()

            List(followers_list, if_list_is_empty_message='Não há Seguidores para serem exibidos').run()

            ViewPartition().border_divisory()

            print('Caso deseje visualizar algum usuário, selecione ele pelo número ao lado')
            print('Para retornar basta manter o campo vazio e pressionar Enter')

            return InputField().show('>>')

      def selection(self, selected_option, perfil_user):
            if not perfil_user:
                  return {'command': 'home_logged_perfil', 'object': None} 

            perfil_belongs_to_logged_user = True if self.logged_user.user_name == perfil_user.user_name else False
            selected_option = selected_option.upper()
            
            if   selected_option in ['1']:
                  pass

            elif selected_option in ['2']:
                  followers_list = Follow().get_user_followers(perfil_user)
                  selected_user_index = self._show_followers_list(followers_list)

                  if self._empty_field(selected_user_index):
                        return {'command': 'show_another_perfil', 'object': perfil_user}
                  elif not self._is_out_of_bounds(selected_user_index, len(followers_list)):
                        return {'command': 'show_another_perfil', 'object': followers_list[selected_user_index-1]}
                  else:
                        return {'command': 'show_another_perfil', 'object': perfil_user}

            elif selected_option in ['3']:
                  pass

            elif selected_option in ['4']:
                  user_selected_on_search = SearchUser(self.logged_user).run()

                  return {'command': 'show_another_perfil', 'object': user_selected_on_search}

            elif selected_option in ['5']:
                  pass

            elif perfil_belongs_to_logged_user and selected_option.upper in ['N']:
                  pass

            elif perfil_belongs_to_logged_user and selected_option in ['D']:
                  return {'command': 'outside_account', 'object': None} 

            elif not perfil_belongs_to_logged_user and selected_option in ['S']:
                  if Follow().follow_exist(self.logged_user, perfil_user):
                        Follow().delete_instance(self.logged_user, perfil_user)
                  else:
                        Follow().create_instance(self.logged_user, perfil_user)
                  
                  return {'command': 'show_another_perfil', 'object': perfil_user}

            elif not perfil_belongs_to_logged_user and selected_option in ['B']:
                  pass

            elif not perfil_belongs_to_logged_user and selected_option in ['R']:
                  return {'command': 'home_logged_perfil', 'object': None} 

            else:
                  return {'command': 'wrong_selection', 'object': perfil_user, 'information message': 'Escolha inválida, tente novamente'}