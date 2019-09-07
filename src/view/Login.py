
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from view.ViewPartition import ViewPartition

class Login():
    def show(self):
        ViewPartition().simplest_divisory()

        while True:
            print("Preencha seus dados de forma correta:")
            user_name = input("Nome de Usuário:")
            password = input("Senha:")

            if True:
                break

        ViewPartition().simplest_divisory()

        


