from passlib.context import CryptContext

password_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return password_hash.hash(password)


def verify(plain_password, hased_password):
    return password_hash.verify(plain_password, hased_password)