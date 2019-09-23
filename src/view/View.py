class View:
    def _is_empty_field(self, field_value):
        if field_value in [None, ''] or (isinstance(field_value, str) and field_value.isspace()):
            return True
        else:
            return False

    def _is_value_a_number(self, value):
        index_as_str_is_digit = True if isinstance(value, str) and value.isdigit() else False
        index_is_number = True if isinstance(value, int) or isinstance(value, float) else False

        return index_is_number or index_as_str_is_digit

    def _is_out_of_bounds(self, index, upper_limit):
        if self._is_value_a_number(index) and 0 <= int(index) < upper_limit:
            return False
        else:
            return True

    def _filter_selected_value(self, selected_value):
        if isinstance(selected_value, str):
            if selected_value.isdigit():
                return selected_value
            else:
                return selected_value.upper()
        else:
            return None

    def _filter_selected_index(self, selected_index):
        if isinstance(selected_index, str) and selected_index.isdigit():
            return int(selected_index) - 1
        else:
            return selected_index


class UserView(View):
    def __init__(self, logged_user, displayed_user=None, displayed_post=None):
        self.logged_user = logged_user
        self.displayed_user = displayed_user
        self.displayed_post = displayed_post

    def _displayed_user_is_logged_user(self):
        return True if self.logged_user == self.displayed_user else False
