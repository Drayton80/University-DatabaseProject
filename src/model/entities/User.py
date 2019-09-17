class User:
    def __init__(self, user_as_list):
        if user_as_list:
            self.user_name = user_as_list[0]
            self.complete_name = user_as_list[1]
            self.password = user_as_list[2]
            self.biography = user_as_list[3]
            self.privacy = user_as_list[4]
