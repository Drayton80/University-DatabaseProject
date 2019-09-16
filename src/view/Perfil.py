import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from view.ViewPartition import ViewPartition
from view.Menus import Menus

class Perfil:
    def show(self, user, information_message=None):
        ViewPartition().border_logo()

        print("Nome de Usuário: " + str(user.user_name)     + "\n" \
              "Nome Real: "       + str(user.complete_name) + "\n" \
              "Biografia:\n"      + str(user.biography)            )

        print("POSTAGENS")
        
        print("O que gostaria de fazer? Escolha uma das opcoes abaixo:\n" \
              " 1 - Para Login                                        \n" \
              " 2 - Para Registrar-se                                 \n" \
              " 3 - Para Sair                                           " )

        ViewPartition().border_information_message(information_message)

    