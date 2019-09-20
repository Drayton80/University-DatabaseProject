class InvalidUsernameException(Exception):       
    def __str__(self):
        return "O nome de usuário apenas pode conter letras, números e o underline"