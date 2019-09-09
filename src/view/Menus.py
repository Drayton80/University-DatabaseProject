import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from view.ViewPartition import ViewPartition

class Menus:
    def _show_information_message(self, information_message=None):
        if information_message:
            ViewPartition().border_divisory()
            print(information_message)
            

    def show_start_menu(self, information_message=None):
        ViewPartition().border_logo()

        print("O que gostaria de fazer? Escolha uma das opcoes abaixo:\n" \
              " 1 - Para Login                                        \n" \
              " 2 - Para Registrar-se                                 \n" \
              " 3 - Para Sair                                           " )

        self._show_information_message(information_message)

    def show_logged_menu(self, user_name=None, information_message=None):
        ViewPartition().border_logo()

        if not user_name:
            user_name = ""

        print("Bem-vindo, " + str(user_name) + "                    \n\n" \
              "O que gostaria de fazer? Escolha uma das opcoes abaixo:\n" \
              " 1 - Visualizar Perfil                                 \n" \
              " 2 - Ver Usuários que Segue                            \n" \
              " 3 - Ver Seguidores                                    \n" \
              " 4 - Buscar Usuários                                   \n" \
              " 5 - Sair da Conta                                     \n" )

        self._show_information_message(information_message)

    