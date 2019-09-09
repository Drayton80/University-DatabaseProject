class WrongPasswordException(Exception):   
    def __str__(self):
        return "Senha incorreta, tente novamente"