
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from model.Accounts import Accounts
from model.entities.User import User

from view.Menus import Menus
from view.Login import Login
from view.Register import Register
from view.Perfil import Perfil
from view.ViewPartition import ViewPartition
from view.InputField import InputField

from control.exceptions.EmptyFieldException import EmptyFieldException


class Main():
    current_logged_user = None
    
    def outside_account(self):
        Menus().show_start_menu()

        while True:
            user_input = InputField().show(">> ")

            if user_input == '1':
                try:
                    self.current_logged_user = Login().show()
                    break

                except EmptyFieldException:
                    Menus().show_start_menu()
                    continue
                
            elif user_input == '2':
                try:
                    self.current_logged_user = Register().show()
                    break

                except EmptyFieldException:
                    Menus().show_start_menu()
                    continue

            elif user_input == '3':
                ViewPartition().clear_console()
                return True
            else:
                Menus().show_start_menu(information_message="Escolha inválida, tente novamente")


    def inside_account(self):
        Perfil().show(self.current_logged_user)
        
        while True:
            user_input = InputField().show(">> ")

            if user_input == '1':
                continue
            elif user_input == '2':
                continue
            elif user_input == '3':
                continue
            elif user_input == '4':
                ViewPartition().clear_console()
                print('busque usuário')
                user_input = InputField().show(">> ")
                print(Accounts().search_users(user_input))
            elif user_input == '5':
                ViewPartition().clear_console()
                break
            else:
                Menus().show_logged_menu(user_name=str(self.current_logged_user[0][0]), information_message="Escolha inválida, tente novamente")

    def run(self):
        ViewPartition().clear_console()

        exit_program = False

        while True:
            exit_program = self.outside_account()

            if not exit_program:
                self.inside_account()
            else:
                break

Main().run()