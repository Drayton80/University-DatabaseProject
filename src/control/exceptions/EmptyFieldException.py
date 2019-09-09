class EmptyFieldException(Exception):
    def __init__(self, field_name):
        self.field_name = field_name
    
    def __str__(self):
        return "O campo " + self.field_name + " está vazio"