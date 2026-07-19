from fastapi import APIRouter,HTTPException,Depends,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime,timedelta
from database import get_db
from models.user import User
from schemas import UserSignup,UserLogin,UserResponse,Token
import os
from dotenv import load_dotenv
load_dotenv()

router=APIRouter(prefix="/auth",tags=["auth"])
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"
#idi mana standard secured signed algo...HMAC with SHA-256 anamata

TOKEN_EXPIRE_DAYS=7

security=HTTPBearer()
#idi expects a bearer token in the authorization header ..only ahh token ey teeskoni mana endpoint ku isthundi which our user is accessing ..so appudu it verifies later..
# eppudaithe fastapi idhi run chesthundho appudu manaki adhi Authorization: Bearer eyJhbGc...  ala read chesi oka obj create chestundi called credentials..aaah credentials ane obj looks like : #HTTPAuthorizationCredentials(
#     scheme="Bearer",
#     credentials="eyJhbGc..."
# ) tarvata manam credentials.credentials ani rastam ante it gives that eyJhbcc...adhii mana actual token string ANAMATA..

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

def create_token(data:dict)->str:
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(days=TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp":expire})
    token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

def get_current_user(
    credentials:HTTPAuthorizationCredentials=Depends(security),
    db:Session=Depends(get_db)
):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload=jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email:str=payload.get("sub")
        #manam mana token ni create chesinappudu we have stored the email in sub ane key value ..

        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user=db.query(User).filter(User.email==email).first()

    if user is None:
        raise credentials_exception
    
    return user

@router.post("/signup",response_model=UserResponse)
def signup(user_data:UserSignup,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.email==user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password=hash_password(user_data.password)
    new_user=User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login",response_model=Token)
def login(user_data:UserLogin,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==user_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    token=create_token({"sub":user.email})
    return {
    "access_token": token,   
    "token_type": "bearer"
}
