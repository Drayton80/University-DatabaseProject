from view.View import View

class List(View):
    def __init__(self, entities_list, if_list_is_empty_message=None, separator='', index_left_list_element=True, word_before_index=''):
        self.entities_list = entities_list
        self.if_list_is_empty_message = if_list_is_empty_message
        self.separator = separator
        self.index_left_list_element = index_left_list_element
        self.word_before_index = word_before_index

    def run(self):
        if not self.entities_list and self.if_list_is_empty_message:
            print(self.if_list_is_empty_message)

        for index in range(len(self.entities_list)):
            index_correction = index+1

            if self.index_left_list_element:
                print(' ' + self.word_before_index + str(index_correction) + ' - ' + str(self.entities_list[index]) + self.separator)
            else:
                print(' '  + self.word_before_index + str(index_correction) + ':')
                print('  ' + str(self.entities_list[index]) + self.separator)