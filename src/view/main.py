
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
    def __init__(self):
        self.current_logged_user = None
    

    def outside_account(self):
        Menus().show_start_menu()

        while True:
            user_input = InputField().show(">> ").lower()

            if user_input in ['login', '1']:
                try:
                    self.current_logged_user = Login().show()
                    return 'home_logged_perfil'

                except EmptyFieldException:
                    Menus().show_start_menu()
                    continue
                
            elif user_input in ['registrar', '2']:
                try:
                    self.current_logged_user = Register().show()
                    return 'home_logged_perfil'

                except EmptyFieldException:
                    Menus().show_start_menu()
                    continue

            elif user_input in ['sair', '3']:
                ViewPartition().clear_console()
                return 'exit'
            else:
                Menus().show_start_menu(information_message="Escolha inválida, tente novamente")


    def run(self):
        ViewPartition().clear_console()

        return_command = 'outside_account'

        while True:
            if   return_command == 'outside_account':
                return_command = self.outside_account()
            
            elif return_command == 'home_logged_perfil':
                return_command = Perfil(self.current_logged_user).run()

            elif return_command == 'exit':
                break

Main().run()

# main (loop) -> Perfil (loop) -> Search -> Perfil (loop)