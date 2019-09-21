class List:
    def __init__(self, entities_list, if_list_is_empty_message=None):
        self.entities_list = entities_list
        self.if_list_is_empty_message = if_list_is_empty_message

    def run(self):
        if not self.entities_list and self.if_list_is_empty_message:
            print(self.if_list_is_empty_message)

        for index in range(len(self.entities_list)):
            index_correction = index+1

            print(' ' + str(index_correction) + ' - ' + str(self.entities_list[index]))