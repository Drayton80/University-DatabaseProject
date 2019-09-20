import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from view.ViewPartition import ViewPartition

class InputField:
    def show(self, left_text, show_divisory=True):
        if show_divisory:
            ViewPartition().border_divisory()

        user_input = input(left_text if left_text.endswith(' ') else left_text + ' ')

        return user_input