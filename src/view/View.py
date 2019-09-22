class View:
    def _is_empty_field(self, field_value):
        if field_value.isspace() or field_value in [None, '']:
            return True
        else:
            return False

    def _is_out_of_bounds(self, index, upper_limit):
        if index.isdigit() and 0 <= int(index)-1 < upper_limit:
            return False
        else:
            return True

class UserView(View):
    def __init__(self, logged_user, displayed_user=None):
        self.logged_user = logged_user
        self.displayed_user = displayed_user

    def _displayed_user_is_logged_user(self):
        return True if self.logged_user == self.displayed_user else False