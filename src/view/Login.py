import os
import sys
import traceback

sys.path.append(os.path.abspath(os.path.join('..')))

from view.ViewPartition import ViewPartition
from view.InputField import InputField

from model.Accounts import Accounts

from control.Validator import Validator
from control.exceptions.EmptyFieldException import EmptyFieldException
from control.exceptions.WrongPasswordException import WrongPasswordException

class Login():
    def show(self):
        ViewPartition().border_logo()
        print("Preencha os campos de Login (deixe-os vazio caso queira retornar ao menu)")
        
        while True:
            try:
                user_name = InputField().show("Nome de Usuário> ")
                user_name = Validator().validate_empty_field(user_name, "Nome de Usuário")

                password  = InputField().show("Senha> ", show_divisory=False)
                password  = Validator().validate_empty_field(password, "Senha")
            
                user = Accounts().login_user(user_name, password)

                if not user:
                    ViewPartition().border_logo()
                    print("Está conta não existe, tente novamente")
                    continue
                else:
                    return user
                
            except WrongPasswordException:
                ViewPartition().border_logo()
                print("Senha incorreta, por favor, tente novamente")

            except EmptyFieldException as exception:
                raise EmptyFieldException(exception.field_name)

            except ValueError:
                ViewPartition().border_logo()
                print("Alguns dos caracteres não são permitidos")

            except Exception:
                ViewPartition().border_logo()
                traceback.print_exc()
                print("Algo deu errado, tente novamente")

