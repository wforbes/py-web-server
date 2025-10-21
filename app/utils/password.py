"""
Password hashing and verification utilities using argon2.

This module provides secure password hashing using the argon2-cffi library,
which implements the Argon2 password hashing algorithm - winner of the
Password Hashing Competition.
"""

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError


# Initialize the PasswordHasher with default secure parameters
# The defaults are appropriate for most use cases and provide good security
_password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hash a plain text password using Argon2.
    
    This function takes a plain text password and returns a secure hash
    that can be safely stored in the database. The hash includes the salt
    and all parameters needed for verification.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        The hashed password as a string (includes salt and parameters)
        
    Example:
        >>> hashed = hash_password("MySecurePassword123")
        >>> print(hashed[:10])  # First 10 chars
        $argon2id$
    """
    return _password_hasher.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    """
    Verify a password against a hash.
    
    This function checks if a plain text password matches a stored hash.
    It handles all argon2 exceptions and returns a simple boolean result.
    
    Args:
        password_hash: The stored password hash from the database
        password: The plain text password to verify
        
    Returns:
        True if the password matches the hash, False otherwise
        
    Example:
        >>> hashed = hash_password("MySecurePassword123")
        >>> verify_password(hashed, "MySecurePassword123")
        True
        >>> verify_password(hashed, "WrongPassword")
        False
    """
    try:
        # verify() raises VerifyMismatchError if password doesn't match
        _password_hasher.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        # Password doesn't match the hash
        return False
    except InvalidHashError:
        # The hash is malformed or corrupted
        return False
    except Exception:
        # Catch any other unexpected errors and treat as failed verification
        return False

