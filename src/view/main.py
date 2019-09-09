
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from view.Login import Login
from view.Register import Register
from view.ViewPartition import ViewPartition
from view.InputField import InputField

from control.exceptions.EmptyFieldException import EmptyFieldException

current_logged_user = None

start_menu = "O que gostaria de fazer? Escolha uma das opcoes abaixo:\n" \
             " 1 - Para Login                                        \n" \
             " 2 - Para Registrar-se                                 \n" \
             " 3 - Para Sair                                           "


def outside_account():    
    while True:
        user_input = InputField().show(">> ")

        if user_input == '1':
            try:
                current_logged_user = Login().show()
                print(current_logged_user)
                break
            except EmptyFieldException:
                ViewPartition().border_logo()
                print(start_menu)
                continue
            
        elif user_input == '2':
            try:
                current_logged_user = Register().show()
                print(current_logged_user)
                break
            except EmptyFieldException:
                ViewPartition().border_logo()
                print(start_menu)
                continue

        elif user_input == '3':
            ViewPartition().clear_console()
            return True
        else:
            print("Resposta errada, tente novamente")

def main():
    ViewPartition().clear_console()

    exit_program = False

    while not exit_program:
        ViewPartition().border_logo()
        print(start_menu)
        
        exit_program = outside_account()
    

main()