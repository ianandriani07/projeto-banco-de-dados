from argon2 import PasswordHasher

def gerar_senha(senha):
    password_hasher = PasswordHasher()
    password_hash = password_hasher.hash(senha)
    return password_hash
