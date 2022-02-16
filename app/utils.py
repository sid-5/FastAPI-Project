from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash(password: str):
    return pwd_context.hash(password)

def verify(in_pass, hashed_pass):
    return pwd_context.verify(in_pass, hashed_pass)