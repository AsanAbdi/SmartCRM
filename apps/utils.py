from fastapi import status, HTTPException


PERMISSION_EXCEPTION = HTTPException(
    detail="Not enough permission", 
    status_code=status.HTTP_400_BAD_REQUEST
)