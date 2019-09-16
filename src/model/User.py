class User:
    def __init__(self, user_as_list):
        if user_as_list:
            self.user_name = user_as_list[0][0]
            self.complete_name = user_as_list[0][1]
            self.password = user_as_list[0][2]
            self.biography = user_as_list[0][3]
            self.privacy = user_as_list[0][4]
        else:
            self.user_name = None
            self.complete_name = None
            self.password = None
            self.biography = None
            self.privacy = None
