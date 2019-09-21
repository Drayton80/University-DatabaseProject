import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from control.exceptions.EmptyFieldException import EmptyFieldException
from control.exceptions.InvalidUsernameException import InvalidUsernameException

class Validator:
    def validate_empty_field(self, field_value, field_name):
        if not field_value or (isinstance(field_value, str) and field_value == ''):
            raise EmptyFieldException(field_name)
        else:
            return field_value

    def validate_user_name_characters(self, user_name):
        search = re.compile(r'[^a-zA-Z0-9_]').search

        if bool(search(user_name)):
            raise InvalidUsernameException()
        else:
            return user_name
