from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta


# FastAPI App

app = FastAPI(
    title="User Authentication API",
    description="Simple FastAPI authentication system",
    version="1.0.0"
)


# JWT Configuration

SECRET_KEY = "my-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


# Password Hashing


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# OAuth2

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


users = {}


# Pydantic Models

class UserRegister(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=30
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=6,
        max_length=100
    )


class UserResponse(BaseModel):

    username: str
    email: EmailStr


class LoginRequest(BaseModel):

    username: str
    password: str


class TokenResponse(BaseModel):

    access_token: str
    token_type: str


# Helper Functions


def hash_password(password: str) -> str:

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(username: str):

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# Authentication Dependency

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token.",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:

        raise credentials_exception

    user = users.get(username)

    if user is None:
        raise credentials_exception

    return user


# Home

@app.get("/")
def home():

    return {
        "message": "User Authentication API",
        "endpoints": {
            "POST /register": "Register a new user",
            "POST /login": "Login and receive JWT",
            "GET /users/me": "Protected user information"
        }
    }



# REGISTER
  
@app.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(user: UserRegister):

    # Check duplicate username 
    if user.username in users:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists."
        )

    # Check duplicate email
    email_exists = any(
        existing_user["email"] == user.email
        for existing_user in users.values()
    )

    if email_exists:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered."
        )

    # Hash password before storing
    hashed_password = hash_password(
        user.password
    )

    users[user.username] = {
        "username": user.username,
        "email": str(user.email),
        "password": hashed_password
    }

    return {
        "username": user.username,
        "email": user.email
    }


# LOGIN

@app.post(
    "/login",
    response_model=TokenResponse
)
def login(credentials: LoginRequest):

    user = users.get(credentials.username)

    # User doesn't exist
    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # Wrong password
    if not verify_password(
        credentials.password,
        user["password"]
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # Generate JWT
    access_token = create_access_token(
        credentials.username
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# PROTECTED ROUTE


@app.get(
    "/users/me",
    response_model=UserResponse )
def get_my_information(
    current_user: dict = Depends(get_current_user)
):

    return current_user


# Another Protected Route

@app.get("/protected")
def protected_route(
    current_user: dict = Depends(get_current_user)
):

    return {
        "message": "You are authenticated!",
        "username": current_user["username"]
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )

    {
    "username": "shiva",
    "email": "shiva@gmail.com",
    "password": "1234567"
}