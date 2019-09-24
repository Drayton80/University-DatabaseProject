import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from model.relationships.Follow import Follow
from model.relationships.Block import Block
from model.entities.User import User

from view.View import UserView
from view.InputField import InputField
from view.ViewPartition import ViewPartition
from view.Menus import Menus
from view.List import List
from view.Search import SearchUser, SearchTopic
from view.Create import PostCreate
from view.PostView import PostView
from view.NotificationView import NotificationView

class Perfil(UserView):
      def _show_follow_list(self, follow_list, follow_type='followers'):
            ViewPartition().border_logo()

            emtpy_message_subject = 'Seguidores' if follow_type == 'followers' else 'Usuários que está Seguindo'

            List(follow_list, if_list_is_empty_message='Não há ' + emtpy_message_subject + ' para serem exibidos').run()

            ViewPartition().border_divisory()

            print('Caso deseje visualizar algum usuário, selecione ele pelo número ao lado')
            print('Para retornar basta manter o campo vazio e pressionar Enter')

            return InputField().show('>>')

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

                  elif command_is_string and returned_information['command'] == 'access_user':
                        selected_option = self.show(returned_information['object'])
                        returned_information = self.selection(selected_option, returned_information['object'])

                  elif command_is_string and returned_information['command'] == 'access_post':
                        PostView(self.logged_user, displayed_post=returned_information['object'])._show_selected_post(returned_information['object'])
                        selected_option = self.show(User.get_user_instance(returned_information['object'].author_id))
                        returned_information = self.selection(selected_option, User.get_user_instance(returned_information['object'].author_id))
                  else:
                        selected_option = self.show(self.logged_user)
                        returned_information = self.selection(selected_option, self.logged_user)                 
                        

      def show(self, perfil_user, information_message=None):
            ViewPartition().border_logo()
            
            if not perfil_user:
                  return {'command': 'home_logged_perfil', 'object': None} 

            perfil_belongs_to_logged_user = True if self.logged_user.user_name == perfil_user.user_name else False
            permission_to_access_privacy = perfil_belongs_to_logged_user or not perfil_user.privacy or (
                                           Follow.follow_exist(self.logged_user, perfil_user) and (
                                           Follow.get_follow_instance(self.logged_user.user_name, perfil_user.user_name).confirmation))

            if perfil_belongs_to_logged_user:
                  print("Bem-vindo,", perfil_user.user_name)
                  ViewPartition().border_divisory()
            elif Follow.follow_exist(perfil_user, self.logged_user) and (
                 Follow.get_follow_instance(perfil_user.user_name, self.logged_user.user_name).confirmation == True):
                  print("@" + perfil_user.user_name + " segue você")
                  ViewPartition().border_divisory()

            privacy_status = 'Privado' if perfil_user.privacy else 'Público'

            print("Informações do Perfil " + privacy_status            )   
            print("Nome de Usuário: " + str(perfil_user.user_name)     + "\n" \
                  "Nome Real: "       + str(perfil_user.complete_name) + "\n" \
                  "Biografia: "       + str(perfil_user.biography)     + "  " )
            
            ViewPartition().border_divisory()
            
            print("O que gostaria de fazer? Digite uma das opcoes abaixo:")
            
            if permission_to_access_privacy:
                  print(" 1 - Ver Linha do Tempo    \n" \
                        " 2 - Ver Seguidores        \n" \
                        " 3 - Ver Aqueles que Segue   " )

                  
            print(" 4 - Buscar Perfil         \n" \
                  " 5 - Buscar Tópico           " ) 

            
            if perfil_belongs_to_logged_user:
                  option_nova_postagem = " C - Para Criar uma Nova Postagem  \n"
                  option_notificacoes  = " N - Para Notificações             \n"
                  option_privacidade   = " P - Para tornar seu Perfil Privado\n" if not self.logged_user.privacy else " P - Para tornar seu Perfil Público\n"
                  option_deslogar      = " D - Para sair da Conta              "

                  extra_options = option_nova_postagem + option_notificacoes + option_privacidade + option_deslogar
            else:
                  if Follow.follow_exist(self.logged_user, perfil_user):
                        follow = Follow.get_follow_instance(self.logged_user.user_name, perfil_user.user_name)
                        
                        option_seguir = '' if follow.confirmation == False else ' S - Para deixar de Seguir\n'
                  else:
                        option_seguir   = ' S - Para Seguir\n' 
                  
                  option_bloquear = ' B - Para Bloquear\n' 
                  option_retornar = ' R - Para retornar para seu Perfil' 
                  
                  extra_options = option_seguir + option_bloquear + option_retornar

            print(extra_options)

            ViewPartition().border_information_message(information_message)

            return InputField().show('>>')
            

      def selection(self, selected_option, perfil_user):
            if not perfil_user:
                  return {'command': 'home_logged_perfil', 'object': None} 

            perfil_belongs_to_logged_user = True if self.logged_user.user_name == perfil_user.user_name else False
            permission_to_access_privacy = perfil_belongs_to_logged_user or not perfil_user.privacy or (
                                           Follow.follow_exist(self.logged_user, perfil_user) and (
                                           Follow.get_follow_instance(self.logged_user.user_name, perfil_user.user_name).confirmation))
            selected_option = selected_option.upper()
            
            if   permission_to_access_privacy and selected_option in ['1']:
                  PostView(self.logged_user, perfil_user).run()

            elif permission_to_access_privacy and selected_option in ['2']:
                  followers_list = perfil_user.get_user_followers()
                  selected_user_index = self._filter_selected_index(self._show_follow_list(followers_list, follow_type='followers'))

                  if self._is_empty_field(selected_user_index):
                        return {'command': 'show_another_perfil', 'object': perfil_user}
                  elif not self._is_out_of_bounds(selected_user_index, len(followers_list)):
                        return {'command': 'show_another_perfil', 'object': followers_list[int(selected_user_index)]}
                  else:
                        return {'command': 'show_another_perfil', 'object': perfil_user}

            elif permission_to_access_privacy and selected_option in ['3']:
                  followeds_list = perfil_user.get_user_followeds()
                  selected_user_index = self._filter_selected_index(self._show_follow_list(followeds_list, follow_type='followeds'))

                  if self._is_empty_field(selected_user_index):
                        return {'command': 'show_another_perfil', 'object': perfil_user}
                  elif not self._is_out_of_bounds(selected_user_index, len(followeds_list)):
                        return {'command': 'show_another_perfil', 'object': followeds_list[selected_user_index]}
                  else:
                        return {'command': 'show_another_perfil', 'object': perfil_user}

            elif selected_option in ['4']:
                  user_selected_on_search = SearchUser(self.logged_user).run()

                  return {'command': 'show_another_perfil', 'object': user_selected_on_search}

            elif selected_option in ['5']:
                  post_selected_on_search = SearchTopic(self.logged_user).run()

                  if post_selected_on_search:
                        return {'command': 'access_post', 'object': post_selected_on_search}
                  else:
                        return {'command': 'home_logged_perfil', 'object': None}

            elif perfil_belongs_to_logged_user and selected_option in ['C']:
                  PostCreate(self.logged_user).run()
            
            elif perfil_belongs_to_logged_user and selected_option in ['N']:
                  return NotificationView(self.logged_user).run()

            elif perfil_belongs_to_logged_user and selected_option in ['P']:
                  # Inverte o status de privacidade:
                  privacy_change = False if self.logged_user.privacy == True else True
                  self.logged_user.set_privacy(privacy_change)

                  return {'command': 'home_logged_perfil', 'object': None} 

            elif perfil_belongs_to_logged_user and selected_option in ['D']:
                  return {'command': 'outside_account', 'object': None} 

            elif not perfil_belongs_to_logged_user and selected_option in ['S']:
                  if Follow.follow_exist(self.logged_user, perfil_user) and (
                     Follow.get_follow_instance(self.logged_user.user_name, perfil_user.user_name).confirmation == False):
                        return {'command': 'wrong_selection', 'object': perfil_user, 'information message': 'Escolha inválida, tente novamente'}

                  if Follow.follow_exist(self.logged_user, perfil_user):
                        Follow.delete_instance(self.logged_user, perfil_user)
                  else:
                        Follow.create_instance(self.logged_user, perfil_user)
                  
                  return {'command': 'show_another_perfil', 'object': perfil_user}

            elif not perfil_belongs_to_logged_user and selected_option in ['B']:
                  if Block.block_exist(self.logged_user.user_name, perfil_user.user_name):
                        Block.delete_instance(self.logged_user.user_name, perfil_user.user_name)
                  else:
                        Block.create_instance(self.logged_user.user_name, perfil_user.user_name)
                  return {'command': 'show_another_perfil', 'object': perfil_user}

            elif not perfil_belongs_to_logged_user and selected_option in ['R']:
                  return {'command': 'home_logged_perfil', 'object': None} 

            else:
                  return {'command': 'wrong_selection', 'object': perfil_user, 'information message': 'Escolha inválida, tente novamente'}