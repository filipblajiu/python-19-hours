from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "l525kl141kl4bk2kl4rkml41lkKJKJ4k3j4klKLjri34502k6457-1-0"
ALGORTITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORTITHM)

    return encoded_jwt
