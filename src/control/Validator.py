import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from control.exceptions.EmptyFieldException import EmptyFieldException

class Validator:
    def validate_empty_field(self, field_value, field_name):
        if not field_value or (isinstance(field_value, str) and field_value == ''):
            raise EmptyFieldException(field_name)
        else:
            return field_value