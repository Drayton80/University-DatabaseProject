class Commentary:
    def __init__(self, commentary_as_list):
        if commentary_as_list:
            self.commentary_id = commentary_as_list[0]
            self.post_id = commentary_as_list[1]
            self.author_id = commentary_as_list[2]
            self.date = commentary_as_list[3]
            self.text = commentary_as_list[4]
            

