from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hash passwords
def hash(password: str):
    return pwd_context.hash(password)


# compare hashed passwords for authetication
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) 