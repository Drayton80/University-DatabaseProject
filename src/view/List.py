from view.View import View

class List(View):
    def __init__(self, entities_list, if_list_is_empty_message=None, separator=''):
        self.entities_list = entities_list
        self.if_list_is_empty_message = if_list_is_empty_message
        self.separator = separator

    def run(self):
        if not self.entities_list and self.if_list_is_empty_message:
            print(self.if_list_is_empty_message)

        for index in range(len(self.entities_list)):
            index_correction = index+1

            print(' ' + str(index_correction) + ' - ' + str(self.entities_list[index]) + self.separator)