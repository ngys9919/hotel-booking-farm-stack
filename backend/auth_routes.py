"""
Authentication API routes for user registration, login, and management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Optional

from models import UserCreate, UserLogin, UserResponse
from auth import (
    create_access_token,
    get_current_user,
    Token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from user_db import (
    create_user,
    authenticate_user,
    get_user_by_email,
    user_to_response
)
from database import get_database

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    """
    Register a new user.
    
    Args:
        user_data: User registration data (email, password, full_name)
        
    Returns:
        UserResponse: Created user information (without password)
        
    Raises:
        HTTPException 400: If user already exists
    """
    try:
        db = get_database()
        user = await create_user(db, user_data)
        return user_to_response(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login user and return JWT access token.
    
    Args:
        form_data: OAuth2 form data with username (email) and password
        
    Returns:
        Token: JWT access token and token type
        
    Raises:
        HTTPException 401: If credentials are invalid
    """
    db = get_database()
    user = await authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.post("/login/json", response_model=Token)
async def login_user_json(user_data: UserLogin):
    """
    Login user with JSON body (alternative to OAuth2 form).
    
    Args:
        user_data: User login data (email, password)
        
    Returns:
        Token: JWT access token and token type
        
    Raises:
        HTTPException 401: If credentials are invalid
    """
    db = get_database()
    user = await authenticate_user(db, user_data.email, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user_email: str = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Args:
        current_user_email: Email of the authenticated user (from JWT token)
        
    Returns:
        UserResponse: Current user information
        
    Raises:
        HTTPException 404: If user not found
    """
    db = get_database()
    user = await get_user_by_email(db, current_user_email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user_to_response(user)


@router.get("/verify", response_model=dict)
async def verify_token(current_user_email: str = Depends(get_current_user)):
    """
    Verify if the JWT token is valid.
    
    Args:
        current_user_email: Email of the authenticated user (from JWT token)
        
    Returns:
        dict: Verification status and user email
    """
    return {
        "valid": True,
        "email": current_user_email,
        "message": "Token is valid"
    }
