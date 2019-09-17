class Post:
    def __init_(self, post_as_list):
        if post_as_list:
            self.post_id = post_as_list[0]
            self.date = post_as_list[1]
            self.text = post_as_list[2]
            self.image = post_as_list[3]
            self.author_id = post_as_list[4]
