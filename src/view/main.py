
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from view.Login import Login
from view.ViewPartition import ViewPartition

def main():
    ViewPartition().simplest_divisory()
    print("Bem Vindo ao PostAge")
    ViewPartition().simplest_divisory()

    print(
        "O que gostaria de fazer? Escolha\n",
        " 1 - Para Login                 \n",
        " 2 - Para Registrar-se          \n",
        " 3 - Para Sair                    "
    )

    while True:
        user_input = input("Escolha um valor:")

        if user_input == '1':
            Login().show()
            break
        elif user_input == '2':
            break
        elif user_input == '3':
            return None
        else:
            print("Resposta errada, tente novamente")

main()