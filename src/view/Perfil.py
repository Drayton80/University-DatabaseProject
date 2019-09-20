import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from model.relationships.Follow import Follow

from view.InputField import InputField
from view.ViewPartition import ViewPartition
from view.Menus import Menus

class Perfil:
      def __init__(self, logged_user):
            self.logged_user = logged_user

      def run(self):
            exit_account = False

            while not exit_account:
                  selected_option = self.show(self.logged_user)
                  exit_account = self.selection(selected_option, self.logged_user)

      def show(self, perfil_user, information_message=None):
            ViewPartition().border_logo()

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
            
            print("O que gostaria de visualizar? Digite uma das opcoes abaixo:")
            
            # TODO checar se o usuário é seguidor do perfil_user para ver se isso será exibido:
            if not perfil_user.privacy or (perfil_user.privacy and True):
                  print(" 1 - Postagens                                             \n" \
                        " 2 - Seguidores                                            \n" \
                        " 3 - Aqueles que Segue                                       " )
            
            if perfil_belongs_to_logged_user:
                  option_notificacoes = " N - Para Notificações \n"
                  option_deslogar     = " D - Para sair da Conta"
                  extra_options = option_notificacoes + option_deslogar
            else:
                  option_seguir   = ' S - Para Seguir\n'   
                  option_bloquear = ' B - Para Bloquear\n' 
                  option_retornar = ' R - Para retornar para seu Perfil' 
                  extra_options = option_seguir + option_bloquear + option_retornar

            print(extra_options)

            ViewPartition().border_information_message(information_message)

            return InputField().show('>>')

      def selection(self, selected_option, perfil_user):
            perfil_belongs_to_logged_user = True if self.logged_user.user_name == perfil_user.user_name else False
            selected_option = selected_option.upper()
            
            if   selected_option in ['1']:
                  return False

            elif selected_option in ['2']:
                  self.show(perfil_user, information_message=Follow().get_user_followers(perfil_user))
                  return False

            elif selected_option in ['3']:
                  return False

            elif perfil_belongs_to_logged_user and selected_option in ['N']:
                  return False

            elif perfil_belongs_to_logged_user and selected_option in ['D']:
                  ViewPartition().clear_console()
                  return True

            else:
                  self.show(perfil_user, information_message="Escolha inválida, tente novamente")