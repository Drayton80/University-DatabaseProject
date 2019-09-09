class RepeatedPrimaryKeyException(Exception):
    def __init__(self, primary_key_name=None):
        self.primary_key_name = primary_key_name
    
    def __str__(self):
        if self.primary_key_name:
            return "Chave primária " + self.primary_key_name + " já existe"