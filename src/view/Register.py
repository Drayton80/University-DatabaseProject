import os
import sys
import traceback

sys.path.append(os.path.abspath(os.path.join('..')))

from view.ViewPartition import ViewPartition
from view.InputField import InputField

from model.Accounts import Accounts

from control.Validator import Validator
from control.exceptions.EmptyFieldException import EmptyFieldException
from control.exceptions.RepeatedPrimaryKeyException import RepeatedPrimaryKeyException
from control.exceptions.InvalidUsernameException import InvalidUsernameException

class Register():
    def show(self):
        ViewPartition().border_dialog("Preencha os campos de Registro (deixe-os vazio caso queira retornar ao menu)")
        
        while True:
            try:
                complete_name = InputField().show("Nome Completo> ")
                complete_name = Validator().validate_empty_field(complete_name, "Nome Completo")

                user_name = InputField().show("Nome de Usuário> ", show_divisory=False)
                user_name = Validator().validate_empty_field(user_name, "Nome de Usuário")
                user_name = Validator().validate_user_name_characters(user_name)

                password  = InputField().show("Senha> ", show_divisory=False)
                password  = Validator().validate_empty_field(password, "Senha")
            
                user = Accounts().register_user(user_name, complete_name, password)

                return user

            except EmptyFieldException as exception:
                raise EmptyFieldException(exception.field_name)

            except RepeatedPrimaryKeyException:
                ViewPartition().border_dialog("Nome de Usuário já existe")

            except InvalidUsernameException as e:
                ViewPartition().border_dialog("O nome de usuário apenas pode conter letras, números e o underline")

            except ValueError:
                ViewPartition().border_dialog("Alguns dos caracteres não são permitidos")

            except Exception:
                ViewPartition().border_dialog("Algo deu errado, tente novamente")

        


